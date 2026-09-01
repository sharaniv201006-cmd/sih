# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np

src_path = r"C:\Users\Dell\Desktop\indian_breed_with_state_district.xlsx"
df_raw = pd.read_excel(src_path)
print(f"Loaded source raw dataset: {df_raw.shape}")

column_map = {
    'Animal_ID': 'animal_id',
    'Breed': 'breed',
    'State': 'state',
    'District': 'district',
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

# Numeric Animal ID
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
df['previous_mastitis_history'] = df['previous_mastitis_history'].apply(
    lambda x: 1 if str(x).strip().lower() in ['yes', '1', 'true'] else 0
)

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

# Add farm_id and record_date
df['farm_id'] = 'F' + (df['animal_id'] % 10 + 1).astype(str).str.zfill(2)
df['record_date'] = '2026-09-01'

# Calculate THI
df['temperature_humidity_index'] = (
    0.8 * df['ambient_temperature_c'] +
    (df['relative_humidity_pct'] / 100.0) * (df['ambient_temperature_c'] - 14.4) + 46.4
)

# Abnormal behavior flag
df['abnormal_behavior'] = ((df['mastitis_risk_category'].isin(['High', 'Moderate'])) | (df['body_temperature_c'] > 39.0)).astype(int)

# Save formatted files
os.makedirs("data", exist_ok=True)
os.makedirs("backend/data", exist_ok=True)

df.to_excel("data/mastitis_dataset.xlsx", index=False)
df.to_csv("data/mastitis_dataset.csv", index=False)
df.to_excel("backend/data/mastitis_dataset.xlsx", index=False)
df.to_csv("backend/data/mastitis_dataset.csv", index=False)

print(f"Saved dataset with State & District: {df.shape}")
print("States represented:\n", df['state'].value_counts().to_dict())
