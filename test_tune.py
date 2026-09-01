# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

df = pd.read_excel('data/mastitis_dataset.xlsx')

# Feature Engineering
df['temp_diff'] = df['body_temperature_c'] - df['udder_surface_temperature_c']
df['fever_index'] = (df['body_temperature_c'] > 38.8).astype(int) + (df['udder_surface_temperature_c'] > 34.5).astype(int)

num_cols = [
    'age_years', 'lactation_number', 'days_in_milk', 'previous_mastitis_history',
    'milk_conductivity_mS_cm', 'body_temperature_c', 'udder_surface_temperature_c',
    'milk_yield_kg_day', 'ambient_temperature_c', 'relative_humidity_pct',
    'hygiene_score_0_100', 'temp_diff', 'fever_index', 'temperature_humidity_index'
]
cat_cols = ['breed', 'cmt_test'] if 'cmt_test' in df.columns else ['breed']

X = df[num_cols + cat_cols].copy()
label_map = {'No_Risk': 0, 'Low': 1, 'Moderate': 2, 'High': 3}
y = df['mastitis_risk_category'].map(label_map)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
    ]
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
X_train_t = preprocessor.fit_transform(X_train)
X_test_t = preprocessor.transform(X_test)

for depth in [3, 4, 5]:
    for lr in [0.03, 0.05, 0.1]:
        clf = XGBClassifier(n_estimators=120, max_depth=depth, learning_rate=lr, random_state=42)
        clf.fit(X_train_t, y_train)
        acc = clf.score(X_test_t, y_test)
        print(f"XGB depth={depth}, lr={lr} -> Accuracy: {acc*100:.2f}%")
