# -*- coding: utf-8 -*-
import os, shutil
import pandas as pd
import numpy as np

src_path = r"C:\Users\Dell\Desktop\indian breed.xlsx"
df_raw = pd.read_excel(src_path)
print(f"Loaded source raw dataset: {df_raw.shape}")

# Standardize columns to match our robust schema
column_map = {
    'Animal_ID': 'animal_id',
    'Breed': 'breed',
    'Age_Years': 'age_years',
    'Lactation_Number': 'lactation_number',
    'Days_in_Milk': 'days_in_milk',
    'Mastitis_History': 'previous_mastitis_history',
    'Milk_Conductivity_mS_cm': 'milk_conductivity_mS_cm',
    'Body_Temperature_C': 'body_temperature_c',
    'Udder_Surface_Temperature_C': 'udder_surface_temperature_c',
    'Daily_Milk_Yield_kg_day': 'milk_yield_kg_day',
    'Ambient_Temperature_C': 'ambient_temperature_c',
    'Humidity_Percent': 'relative_humidity_pct',
    'Hygiene_Score': 'hygiene_score_0_100',
    'CMT_Test': 'cmt_test',
    'Mastitis_Risk_Score': 'synthetic_risk_score_pct',
    'Mastitis_Risk': 'mastitis_risk_category'
}

df = df_raw.rename(columns=column_map)

# Extract numeric ID if string (e.g. 'IND10001' -> 10001)
def parse_id(val):
    if isinstance(val, (int, float)):
        return int(val)
    s = str(val).replace('IND', '').replace('#', '').strip()
    try:
        return int(s)
    except:
        return 10000 + np.random.randint(1, 9000)

df['animal_id'] = df['animal_id'].apply(parse_id)

# Standardize boolean and categories
if df['previous_mastitis_history'].dtype == object:
    df['previous_mastitis_history'] = df['previous_mastitis_history'].apply(lambda x: 1 if str(x).lower().startswith('y') else 0)

risk_map = {
    'No Risk': 'No_Risk',
    'Low Risk': 'Low',
    'Moderate Risk': 'Moderate',
    'High Risk': 'High',
    'No_Risk': 'No_Risk',
    'Low': 'Low',
    'Moderate': 'Moderate',
    'High': 'High'
}
df['mastitis_risk_category'] = df['mastitis_risk_category'].map(lambda x: risk_map.get(str(x).strip(), 'No_Risk'))

# Add farm_id and record_date if not present
if 'farm_id' not in df.columns:
    df['farm_id'] = 'F' + (df['animal_id'] % 10 + 1).astype(str).str.zfill(2)
if 'record_date' not in df.columns:
    df['record_date'] = '2026-08-31'

# Calculate THI index
df['temperature_humidity_index'] = (
    0.8 * df['ambient_temperature_c'] +
    (df['relative_humidity_pct'] / 100.0) * (df['ambient_temperature_c'] - 14.4) + 46.4
)

# Abnormal behavior flag based on risk / temp
df['abnormal_behavior'] = ((df['mastitis_risk_category'].isin(['High', 'Moderate'])) | (df['body_temperature_c'] > 39.0)).astype(int)

# Save to data/ and backend/data/
os.makedirs("data", exist_ok=True)
os.makedirs("backend/data", exist_ok=True)

df.to_excel("data/mastitis_dataset.xlsx", index=False)
df.to_csv("data/mastitis_dataset.csv", index=False)
df.to_excel("backend/data/mastitis_dataset.xlsx", index=False)
df.to_csv("backend/data/mastitis_dataset.csv", index=False)

print(f"Successfully formatted and saved new dataset: {df.shape}")
print("Risk breakdown:\n", df['mastitis_risk_category'].value_counts())
print("Unique Breeds in new dataset:\n", df['breed'].value_counts().to_dict())
