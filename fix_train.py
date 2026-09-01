# -*- coding: utf-8 -*-
with open("backend/app/ml/train.py", "w", encoding="utf-8") as f:
    f.write("""import os
import json
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from app.ml.preprocess import (
    create_preprocessor,
    ALL_MODEL_FEATURES,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN,
    LABEL_MAP,
    INV_LABEL_MAP
)

def train_model(data_path=None, model_dir=None):
    if data_path is None:
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '../../../data/mastitis_dataset.xlsx'),
            os.path.join(os.path.dirname(__file__), '../../../data/mastitis_dataset.csv'),
            'data/mastitis_dataset.xlsx',
            'data/mastitis_dataset.csv'
        ]
        for p in possible_paths:
            if os.path.exists(p):
                data_path = p
                break

    if not data_path or not os.path.exists(data_path):
        raise FileNotFoundError(f'Dataset not found at {data_path}')

    if model_dir is None:
        model_dir = os.path.join(os.path.dirname(__file__), 'model')
    os.makedirs(model_dir, exist_ok=True)

    print(f'Loading dataset from {data_path}...')
    if data_path.endswith('.xlsx'):
        df = pd.read_excel(data_path)
    else:
        df = pd.read_csv(data_path)

    print(f'Dataset shape: {df.shape}')
    
    # Coerce numeric columns
    for num_col in NUMERICAL_FEATURES:
        if num_col in df.columns:
            if df[num_col].dtype == object:
                df[num_col] = df[num_col].apply(lambda x: 1 if str(x).lower() in ['yes', '1', 'true'] else 0 if str(x).lower() in ['no', '0', 'false'] else pd.to_numeric(x, errors='coerce'))
            df[num_col] = pd.to_numeric(df[num_col], errors='coerce').fillna(0.0)
        else:
            df[num_col] = 0.0

    # Ensure categorical columns exist
    for cat_col in CATEGORICAL_FEATURES:
        if cat_col in df.columns:
            df[cat_col] = df[cat_col].astype(str).fillna('Unknown')
        else:
            df[cat_col] = 'Unknown'

    X = df[ALL_MODEL_FEATURES].copy()
    y = df[TARGET_COLUMN].map(LABEL_MAP).fillna(0).astype(int).copy()

    # Train / Test split (80/20 stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f'Training samples: {len(X_train)}, Testing samples: {len(X_test)}')

    # Build and fit preprocessing pipeline
    preprocessor = create_preprocessor()
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    # Get feature names after one-hot encoding
    cat_encoder = preprocessor.named_transformers_['cat']
    cat_feature_names = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
    transformed_feature_names = NUMERICAL_FEATURES + cat_feature_names

    # Train XGBoost Classifier
    print('Training XGBoost Multi-class Classifier...')
    model = XGBClassifier(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.08,
        subsample=0.85,
        colsample_bytree=0.85,
        objective='multi:softprob',
        num_class=4,
        random_state=42,
        eval_metric='mlogloss'
    )
    model.fit(X_train_transformed, y_train)

    # Evaluate model
    y_pred = model.predict(X_test_transformed)
    y_pred_proba = model.predict_proba(X_test_transformed)

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
    rec = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
    f1 = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))
    cm = confusion_matrix(y_test, y_pred).tolist()

    class_names = [INV_LABEL_MAP[i] for i in range(4)]
    report = classification_report(y_test, y_pred, target_names=class_names, output_dict=True, zero_division=0)

    print(f'Model Accuracy: {acc * 100:.2f}%')
    print(f'Model Precision: {prec * 100:.2f}%')
    print(f'Model Recall: {rec * 100:.2f}%')
    print(f'Model F1-Score: {f1 * 100:.2f}%')

    # Feature Importance
    importances = model.feature_importances_
    feat_importance = []
    for name, imp in zip(transformed_feature_names, importances):
        feat_importance.append({'feature': name, 'importance': round(float(imp) * 100, 2)})
    feat_importance = sorted(feat_importance, key=lambda x: x['importance'], reverse=True)

    # Save artifacts
    model_path = os.path.join(model_dir, 'mastitis_xgb_model.joblib')
    pipeline_path = os.path.join(model_dir, 'pipeline.joblib')
    metrics_path = os.path.join(model_dir, 'model_metrics.json')
    feat_imp_path = os.path.join(model_dir, 'feature_importance.json')

    joblib.dump(model, model_path)
    joblib.dump(preprocessor, pipeline_path)

    metrics_payload = {
        'model_name': 'XGBoost Multi-Class Bovine Mastitis Risk Classifier (Indian Breeds)',
        'algorithm': 'Extreme Gradient Boosting (XGBoost)',
        'framework': 'xgboost / scikit-learn',
        'training_records': int(len(X_train)),
        'test_records': int(len(X_test)),
        'accuracy': round(acc, 4),
        'precision': round(prec, 4),
        'recall': round(rec, 4),
        'f1_score': round(f1, 4),
        'classes': class_names,
        'confusion_matrix': cm,
        'classification_report': report,
        'transformed_feature_names': transformed_feature_names
    }

    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(metrics_payload, f, indent=2)

    with open(feat_imp_path, 'w', encoding='utf-8') as f:
        json.dump(feat_importance, f, indent=2)

    print(f'Artifacts successfully saved in {model_dir}:')
    print(f' - Model: {model_path}')
    print(f' - Pipeline: {pipeline_path}')
    print(f' - Metrics: {metrics_path}')
    print(f' - Feature Importance: {feat_imp_path}')

    return metrics_payload

if __name__ == '__main__':
    train_model()
""")

print("Updated backend/app/ml/train.py.")
