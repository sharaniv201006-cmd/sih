import os
import joblib
import numpy as np
import pandas as pd

from app.ml.preprocess import (
    ALL_MODEL_FEATURES,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    INV_LABEL_MAP
)

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'mastitis_xgb_model.joblib')
PIPELINE_PATH = os.path.join(MODEL_DIR, 'pipeline.joblib')

_model = None
_pipeline = None

def get_model_and_pipeline():
    global _model, _pipeline
    if _model is None or _pipeline is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(PIPELINE_PATH):
            from app.ml.train import train_model
            train_model()
        _model = joblib.load(MODEL_PATH)
        _pipeline = joblib.load(PIPELINE_PATH)
    return _model, _pipeline

REFERENCE_BASELINES = {
    'body_temperature_c': {'normal_max': 38.8, 'critical': 39.5, 'weight': 1.8, 'label': 'Elevated Body Temperature'},
    'udder_surface_temperature_c': {'normal_max': 34.2, 'critical': 35.5, 'weight': 2.0, 'label': 'Elevated Udder Surface Temperature'},
    'milk_conductivity_mS_cm': {'normal_max': 4.3, 'critical': 5.2, 'weight': 2.5, 'label': 'High Milk Electrical Conductivity (Ion leakage)'},
    'milk_yield_kg_day': {'normal_min': 15.0, 'critical': 10.0, 'weight': 1.4, 'label': 'Sudden Milk Yield Drop'},
    'hygiene_score_0_100': {'normal_min': 65.0, 'critical': 40.0, 'weight': 1.3, 'label': 'Poor Barn/Teat Hygiene Score'},
    'environment_total_mastitis_pathogen_load_log10': {'normal_max': 4.5, 'critical': 5.5, 'weight': 1.6, 'label': 'High Environmental Pathogen Exposure'},
    'S_aureus_load_log10_cfu_equiv': {'normal_max': 4.0, 'critical': 5.0, 'weight': 1.5, 'label': 'Elevated S. aureus Proxy Load'},
    'S_uberis_load_log10_cfu_equiv': {'normal_max': 4.0, 'critical': 5.0, 'weight': 1.5, 'label': 'Elevated S. uberis Proxy Load'},
    'E_coli_load_log10_cfu_equiv': {'normal_max': 4.0, 'critical': 5.0, 'weight': 1.5, 'label': 'Elevated E. coli Proxy Load'},
    'previous_mastitis_history': {'normal_max': 0, 'critical': 1, 'weight': 1.2, 'label': 'Prior History of Mastitis Episode'},
    'ambient_temperature_c': {'normal_max': 28.0, 'critical': 35.0, 'weight': 1.1, 'label': 'Heat Stress Environmental Condition'},
    'relative_humidity_pct': {'normal_max': 70.0, 'critical': 85.0, 'weight': 1.1, 'label': 'High Ambient Barn Humidity'}
}

def analyze_risk_factors(data_dict):
    factors = []
    for key, rule in REFERENCE_BASELINES.items():
        val = data_dict.get(key)
        if val is None:
            continue
        try:
            val = float(val)
        except (ValueError, TypeError):
            continue
        impact_score = 0.0
        details = ''
        if 'normal_max' in rule and val > rule['normal_max']:
            excess = (val - rule['normal_max']) / (rule['critical'] - rule['normal_max'] + 1e-5)
            impact_score = min(excess * rule['weight'], 3.0)
            norm_max = rule['normal_max']
            details = f'{val:.2f} (Threshold: <= {norm_max})'
        elif 'normal_min' in rule and val < rule['normal_min']:
            deficit = (rule['normal_min'] - val) / (rule['normal_min'] - rule['critical'] + 1e-5)
            impact_score = min(deficit * rule['weight'], 3.0)
            norm_min = rule['normal_min']
            details = f'{val:.2f} (Threshold: >= {norm_min})'

        if impact_score > 0.3:
            factors.append({
                'factor': rule['label'],
                'feature_name': key,
                'observed_value': val,
                'impact_score': round(impact_score, 2),
                'details': details
            })
    factors = sorted(factors, key=lambda x: x['impact_score'], reverse=True)
    return factors[:5]

def generate_recommendations(risk_category, top_factors, env_risk_favorable):
    recs = []
    if risk_category in ['High', 'Moderate']:
        recs.append('Conduct on-farm California Mastitis Test (CMT) or individual quarter conductivity check during next milking.')
        recs.append('Isolate milk from this cow until subclinical status is cleared.')
        recs.append('Inspect teat skin integrity, pre-dip contact time, and post-milking barrier teat dip application.')
    else:
        recs.append('Maintain standard milking hygiene and scheduled herd health monitoring.')

    if env_risk_favorable:
        recs.append('Environmental conditions (heat/humidity index) favor pathogen proliferation: increase stall bedding replacement and ventilation.')

    has_temp_issue = any('Temperature' in f.get('factor', '') for f in top_factors)
    if has_temp_issue and risk_category == 'High':
        recs.append('Elevated biometric temperature detected: check for systemic clinical signs (swollen quarters, appetite loss, rectal temp).')

    recs.append('Note: These recommendations serve as decision-support alerts and do not replace professional veterinary clinical diagnosis.')
    return recs

def predict_single_animal(data: dict):
    model, pipeline = get_model_and_pipeline()

    row_dict = {}
    for feat in ALL_MODEL_FEATURES:
        if feat in data and data[feat] is not None:
            row_dict[feat] = data[feat]
        elif feat in NUMERICAL_FEATURES:
            row_dict[feat] = 0.0
        else:
            row_dict[feat] = 'Unknown'

    input_df = pd.DataFrame([row_dict])
    transformed_input = pipeline.transform(input_df)
    pred_class_idx = int(model.predict(transformed_input)[0])
    probabilities = model.predict_proba(transformed_input)[0]
    
    risk_category = INV_LABEL_MAP[pred_class_idx]
    
    class_weights = np.array([0.05, 0.32, 0.68, 0.95])
    raw_risk_score = float(np.sum(probabilities * class_weights) * 100.0)
    risk_score = round(max(1.0, min(99.0, raw_risk_score)), 1)
    
    class_probs = {
        INV_LABEL_MAP[i]: round(float(probabilities[i]) * 100.0, 1)
        for i in range(4)
    }

    top_factors = analyze_risk_factors(data)

    amb_temp = float(data.get('ambient_temperature_c', 25.0) or 25.0)
    rel_hum = float(data.get('relative_humidity_pct', 60.0) or 60.0)
    thi = 0.8 * amb_temp + (rel_hum / 100.0) * (amb_temp - 14.4) + 46.4
    env_risk_favorable = bool(thi >= 72.0 or (amb_temp >= 28.0 and rel_hum >= 75.0))

    env_indicator = {
        'ambient_temperature_c': amb_temp,
        'relative_humidity_pct': rel_hum,
        'calculated_thi': round(thi, 1),
        'conditions_favorable_for_pathogens': env_risk_favorable,
        'interpretation': 'Elevated heat/humidity index associates with increased bacterial proliferation risk in bedding' if env_risk_favorable else 'Barn environmental temperature and humidity are within optimal range'
    }

    forecast_7d_prob = round(float(probabilities[2] * 0.4 + probabilities[3] * 0.85) * 100, 1)
    forecast_14d_prob = round(float(probabilities[1] * 0.2 + probabilities[2] * 0.65 + probabilities[3] * 0.92) * 100, 1)

    recommendations = generate_recommendations(risk_category, top_factors, env_risk_favorable)

    return {
        'animal_id': str(data.get('animal_id', 'SIMULATED_COW')),
        'risk_category': risk_category,
        'risk_score': risk_score,
        'class_probabilities': class_probs,
        'top_risk_factors': top_factors,
        'forecast_7d_risk_pct': forecast_7d_prob,
        'forecast_14d_risk_pct': forecast_14d_prob,
        'environmental_risk': env_indicator,
        'recommendations': recommendations
    }
