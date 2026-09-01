# -*- coding: utf-8 -*-
# Update backend/app/ml/preprocess.py
with open("backend/app/ml/preprocess.py", "w", encoding="utf-8") as f:
    f.write("""import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

NUMERICAL_FEATURES = [
    'age_years',
    'lactation_number',
    'days_in_milk',
    'previous_mastitis_history',
    'milk_conductivity_mS_cm',
    'body_temperature_c',
    'udder_surface_temperature_c',
    'milk_yield_kg_day',
    'ambient_temperature_c',
    'relative_humidity_pct',
    'hygiene_score_0_100'
]

CATEGORICAL_FEATURES = [
    'breed'
]

ALL_MODEL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

TARGET_COLUMN = 'mastitis_risk_category'

LABEL_MAP = {
    'No_Risk': 0,
    'Low': 1,
    'Moderate': 2,
    'High': 3
}

INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}

def create_preprocessor():
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERICAL_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ],
        remainder='drop'
    )
    return preprocessor
""")

print("Updated preprocess.py for Indian breed dataset.")
