# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

for p in ["data/mastitis_dataset.xlsx", "backend/data/mastitis_dataset.xlsx", "data/mastitis_dataset.csv", "backend/data/mastitis_dataset.csv"]:
    if p.endswith('.xlsx'):
        df = pd.read_excel(p)
    else:
        df = pd.read_csv(p)
    
    # Clean boolean fields
    df['previous_mastitis_history'] = df['previous_mastitis_history'].apply(lambda x: 1 if str(x).strip().lower() in ['yes', '1', 'true'] else 0)
    df['abnormal_behavior'] = df['abnormal_behavior'].apply(lambda x: 1 if str(x).strip().lower() in ['yes', '1', 'true'] else 0)
    
    if p.endswith('.xlsx'):
        df.to_excel(p, index=False)
    else:
        df.to_csv(p, index=False)

print("Cleaned datasets.")
