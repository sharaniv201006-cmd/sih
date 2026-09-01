# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.config import settings
from app.ml.predict import predict_single_animal

_df_cache = None

def sanitize_record(record: dict) -> dict:
    sanitized = {}
    for k, v in record.items():
        if pd.isna(v) or v is np.nan:
            sanitized[k] = None
        else:
            sanitized[k] = v
    return sanitized

def load_dataset() -> pd.DataFrame:
    global _df_cache
    if _df_cache is not None:
        return _df_cache
    candidate_paths = [
        settings.DATA_FILE_PATH,
        os.path.join(os.path.dirname(__file__), "../../../data/mastitis_dataset.xlsx"),
        os.path.join(os.path.dirname(__file__), "../../../data/mastitis_dataset.csv"),
        "data/mastitis_dataset.xlsx",
        "data/mastitis_dataset.csv"
    ]
    found_path = None
    for p in candidate_paths:
        if os.path.exists(p):
            found_path = p
            break
    if not found_path:
        raise FileNotFoundError("Dataset not found in data/ folder.")
    print(f"[DataService] Loading dataset from: {found_path}")
    if found_path.endswith(".xlsx"):
        df = pd.read_excel(found_path)
    else:
        df = pd.read_csv(found_path)
    df["animal_id"] = df["animal_id"].astype(int)
    df["record_date"] = df["record_date"].astype(str)
    if "temperature_humidity_index" not in df.columns:
        df["temperature_humidity_index"] = (
            0.8 * df["ambient_temperature_c"] +
            (df["relative_humidity_pct"] / 100.0) * (df["ambient_temperature_c"] - 14.4) + 46.4
        )
    _df_cache = df
    print(f"[DataService] Dataset loaded: {len(df)} rows, {len(df.columns)} columns.")
    return _df_cache

import threading

def _save_to_disk_bg(df_copy):
    try:
        excel_path = os.path.join(os.path.dirname(__file__), "../../../data/mastitis_dataset.xlsx")
        csv_path = os.path.join(os.path.dirname(__file__), "../../../data/mastitis_dataset.csv")
        # Save CSV instantly
        df_copy.to_csv(csv_path, index=False)
        # Save Excel in background thread
        df_copy.to_excel(excel_path, index=False)
        print(f"[DataService] Dataset persisted to {csv_path} and {excel_path}")
    except Exception as e:
        print(f"[DataService] Warning saving dataset: {e}")

def persist_dataset():
    global _df_cache
    if _df_cache is None:
        return
    df_copy = _df_cache.copy()
    threading.Thread(target=_save_to_disk_bg, args=(df_copy,), daemon=True).start()

def get_dashboard_summary() -> Dict[str, Any]:
    df = load_dataset()
    total = len(df)
    counts = df["mastitis_risk_category"].value_counts().to_dict()
    no_risk = int(counts.get("No_Risk", 0))
    low_risk = int(counts.get("Low", 0))
    mod_risk = int(counts.get("Moderate", 0))
    high_risk = int(counts.get("High", 0))

    dist_pct = {
        "No_Risk": round((no_risk / total) * 100, 1),
        "Low": round((low_risk / total) * 100, 1),
        "Moderate": round((mod_risk / total) * 100, 1),
        "High": round((high_risk / total) * 100, 1)
    }

    herd_averages = {
        "avg_body_temp": round(float(df["body_temperature_c"].mean()), 2),
        "avg_udder_temp": round(float(df["udder_surface_temperature_c"].mean()), 2),
        "avg_milk_conductivity": round(float(df["milk_conductivity_mS_cm"].mean()), 2),
        "avg_milk_yield": round(float(df["milk_yield_kg_day"].mean()), 2),
        "avg_hygiene_score": round(float(df["hygiene_score_0_100"].mean()), 1),
        "avg_risk_score": round(float(df["synthetic_risk_score_pct"].mean()), 1)
    }

    avg_amb_temp = float(df["ambient_temperature_c"].mean())
    avg_rel_hum = float(df["relative_humidity_pct"].mean())
    avg_thi = float(df["temperature_humidity_index"].mean())
    env_favorable = bool(avg_thi >= 72.0 or (avg_amb_temp >= 28.0 and avg_rel_hum >= 75.0))

    env_status = {
        "ambient_temperature_c": round(avg_amb_temp, 1),
        "relative_humidity_pct": round(avg_rel_hum, 1),
        "average_thi": round(avg_thi, 1),
        "pathogen_proliferation_risk": "Elevated" if env_favorable else "Normal",
        "conditions_favorable_for_pathogens": env_favorable
    }

    high_df = df[df["mastitis_risk_category"] == "High"].sort_values("synthetic_risk_score_pct", ascending=False).head(10)
    alerts = []
    for _, row in high_df.iterrows():
        top_reasons = []
        if row["milk_conductivity_mS_cm"] > 4.5:
            top_reasons.append(f"Conductivity: {row['milk_conductivity_mS_cm']:.2f} mS/cm")
        if row["body_temperature_c"] > 39.0:
            top_reasons.append(f"Body Temp: {row['body_temperature_c']:.2f} C")
        if row["udder_surface_temperature_c"] > 34.5:
            top_reasons.append(f"Udder Temp: {row['udder_surface_temperature_c']:.2f} C")
        if not top_reasons:
            top_reasons.append("Elevated pathogen proxy load")

        alerts.append({
            "animal_id": int(row["animal_id"]),
            "farm_id": str(row["farm_id"]),
            "record_date": str(row["record_date"]),
            "breed": str(row["breed"]),
            "risk_score": round(float(row["synthetic_risk_score_pct"]), 1),
            "risk_category": "High",
            "body_temperature_c": round(float(row["body_temperature_c"]), 2),
            "milk_conductivity_mS_cm": round(float(row["milk_conductivity_mS_cm"]), 2),
            "udder_surface_temperature_c": round(float(row["udder_surface_temperature_c"]), 2),
            "top_factors": top_reasons[:3],
            "alert_level": "CRITICAL",
            "recommendation": "Isolate quarter milk and perform on-farm CMT; consult herd veterinarian."
        })

    recent_records = [sanitize_record(r) for r in df.head(15).to_dict(orient="records")]

    return {
        "total_animals": total,
        "no_risk_count": no_risk,
        "low_risk_count": low_risk,
        "moderate_risk_count": mod_risk,
        "high_risk_count": high_risk,
        "risk_distribution_pct": dist_pct,
        "herd_averages": herd_averages,
        "environmental_status": env_status,
        "recent_high_risk_alerts": alerts,
        "recent_predictions": recent_records
    }

def get_animals_list(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    risk_filter: Optional[str] = None,
    breed_filter: Optional[str] = None,
    sort_by: str = "animal_id",
    sort_order: str = "asc"
) -> Dict[str, Any]:
    df = load_dataset()
    filtered = df.copy()

    if search:
        s = search.strip().lower()
        filtered = filtered[
            filtered["animal_id"].astype(str).str.contains(s) |
            filtered["farm_id"].astype(str).str.lower().contains(s) |
            filtered["breed"].astype(str).str.lower().contains(s)
        ]

    if risk_filter and risk_filter.lower() != "all":
        filtered = filtered[filtered["mastitis_risk_category"].str.lower() == risk_filter.lower()]

    if breed_filter and breed_filter.lower() != "all":
        filtered = filtered[filtered["breed"].str.lower() == breed_filter.lower()]

    ascending = (sort_order.lower() == "asc")
    if sort_by in filtered.columns:
        filtered = filtered.sort_values(sort_by, ascending=ascending)

    total_count = len(filtered)
    total_pages = max(1, int(np.ceil(total_count / page_size)))
    page = max(1, min(page, total_pages))
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    raw_rows = filtered.iloc[start_idx:end_idx].to_dict(orient="records")
    page_rows = [sanitize_record(r) for r in raw_rows]

    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "animals": page_rows
    }

def get_animal_detail(animal_id: int) -> Optional[Dict[str, Any]]:
    df = load_dataset()
    matched = df[df["animal_id"] == animal_id]
    
    if matched.empty:
        return None

    row = sanitize_record(matched.iloc[0].to_dict())
    prediction_result = predict_single_animal(row)

    historical_summary = {
        "total_records_tracked": len(matched),
        "first_recorded_date": str(row.get("record_date", "2026-01-01")),
        "current_status": "Under Observation" if prediction_result["risk_category"] in ["High", "Moderate"] else "Healthy Production",
        "historical_risk_score": round(float(row.get("synthetic_risk_score_pct", 0.0) or 0.0), 1),
        "clinical_flag": int(row.get("clinical_mastitis_now", 0) or 0)
    }

    return {
        "animal": row,
        "prediction": prediction_result,
        "historical_summary": historical_summary
    }

def get_sensor_data_by_id(animal_id: int) -> Optional[Dict[str, Any]]:
    df = load_dataset()
    matched = df[df["animal_id"] == animal_id]
    if matched.empty:
        return None

    row = sanitize_record(matched.iloc[0].to_dict())
    
    curr_body_temp = float(row.get("body_temperature_c", 38.6) or 38.6)
    curr_udder_temp = float(row.get("udder_surface_temperature_c", 33.9) or 33.9)
    curr_cond = float(row.get("milk_conductivity_mS_cm", 4.2) or 4.2)
    curr_yield = float(row.get("milk_yield_kg_day", 15.0) or 15.0)
    risk_cat = str(row.get("mastitis_risk_category", "No_Risk"))

    telemetry_points = []
    days = ["Day -6", "Day -5", "Day -4", "Day -3", "Day -2", "Day -1", "Today"]
    
    # Generate realistic dynamic curve leading up to current reading
    for i, day in enumerate(days):
        ratio = i / 6.0 # 0.0 at Day -6 to 1.0 Today
        
        if risk_cat == "High":
            # Acute onset: began normal, sharply climbed
            start_cond = 3.9
            start_temp = 38.5
            start_yield = curr_yield + 6.5
            c_val = start_cond + (curr_cond - start_cond) * (ratio ** 1.5) + (i % 2) * 0.05
            t_val = start_temp + (curr_body_temp - start_temp) * (ratio ** 1.3) + ((i + 1) % 2) * 0.04
            y_val = max(4.0, start_yield - (start_yield - curr_yield) * (ratio ** 1.2) - (i % 2) * 0.2)
        elif risk_cat == "Moderate":
            # Subclinical drift
            start_cond = 4.0
            start_temp = 38.5
            start_yield = curr_yield + 3.0
            c_val = start_cond + (curr_cond - start_cond) * ratio + (i % 3 - 1) * 0.04
            t_val = start_temp + (curr_body_temp - start_temp) * ratio + (i % 2) * 0.03
            y_val = max(5.0, start_yield - (start_yield - curr_yield) * ratio)
        else:
            # Healthy baseline with natural organic daily fluctuation
            noise_c = ((i * 7) % 5 - 2) * 0.06
            noise_t = ((i * 11) % 5 - 2) * 0.05
            noise_y = ((i * 13) % 5 - 2) * 0.4
            c_val = curr_cond + noise_c
            t_val = curr_body_temp + noise_t
            y_val = curr_yield + noise_y

        telemetry_points.append({
            "day": day,
            "body_temperature_c": round(float(t_val), 2),
            "udder_surface_temperature_c": round(float(curr_udder_temp - (1.0 - ratio) * 0.8), 2),
            "milk_conductivity_mS_cm": round(float(c_val), 2),
            "milk_yield_kg_day": round(float(y_val), 2),
        })

    return {
        "animal_id": animal_id,
        "current_telemetry": row,
        "telemetry_trend": telemetry_points
    }

def register_animal_record(req_data: dict) -> Dict[str, Any]:
    global _df_cache
    df = load_dataset()
    
    animal_id = int(req_data["animal_id"])
    
    # Check for duplicate animal_id
    if animal_id in df["animal_id"].values:
        raise ValueError(f"Animal ID #{animal_id} is already registered in the system.")

    # Behavioral modifier for baseline telemetry
    has_abnormal_behavior = bool(req_data.get("abnormal_behavior", False))
    has_mastitis_history = 1 if req_data.get("previous_mastitis_history", False) else 0

    base_body_temp = 39.2 if has_abnormal_behavior else 38.6
    base_udder_temp = 34.8 if has_abnormal_behavior else 33.8
    base_conductivity = 4.7 if has_abnormal_behavior else 4.0
    base_yield = 11.5 if has_abnormal_behavior else 16.0

    today_str = datetime.now().strftime("%Y-%m-%d")

    new_record = {
        "record_date": today_str,
        "farm_id": "F01",
        "animal_id": animal_id,
        "breed": str(req_data.get("breed", "Jersey_cross")),
        "age_years": float(req_data.get("age_years", 4.0)),
        "lactation_number": int(req_data.get("lactation_number", 2)),
        "days_in_milk": 65,
        "previous_mastitis_history": has_mastitis_history,
        "vaccinated": 1,
        "chronic_disease_flag": 0,
        "ambient_temperature_c": 28.0,
        "relative_humidity_pct": 70.0,
        "hygiene_score_0_100": 60.0,
        "environment_total_mastitis_pathogen_load_log10": 4.5,
        "S_aureus_load_log10_cfu_equiv": 4.0,
        "S_uberis_load_log10_cfu_equiv": 4.1,
        "E_coli_load_log10_cfu_equiv": 3.8,
        "K_pneumoniae_load_log10_cfu_equiv": 3.6,
        "S_agalactiae_load_log10_cfu_equiv": 3.3,
        "dominant_environment_pathogen": "S_uberis",
        "milk_yield_kg_day": base_yield,
        "milk_conductivity_mS_cm": base_conductivity,
        "body_temperature_c": base_body_temp,
        "udder_surface_temperature_c": base_udder_temp,
    }

    # Evaluate through ML model
    pred_res = predict_single_animal(new_record)
    
    new_record["clinical_mastitis_now"] = 1 if pred_res["risk_category"] == "High" else 0
    new_record["synthetic_risk_score_pct"] = pred_res["risk_score"]
    new_record["mastitis_risk_category"] = pred_res["risk_category"]
    new_record["mastitis_in_next_7d"] = 1 if pred_res["forecast_7d_risk_pct"] >= 50.0 else 0
    new_record["mastitis_in_next_14d"] = 1 if pred_res["forecast_14d_risk_pct"] >= 50.0 else 0
    new_record["days_to_synthetic_event"] = None
    new_record["temperature_humidity_index"] = 0.8 * 28.0 + (70.0 / 100.0) * (28.0 - 14.4) + 46.4

    # Add to beginning of DataFrame
    new_df = pd.DataFrame([new_record])
    _df_cache = pd.concat([new_df, df], ignore_index=True)
    
    # Persist dataset
    persist_dataset()

    return {
        "success": True,
        "message": f"Animal #{animal_id} successfully registered and integrated into herd surveillance.",
        "animal": sanitize_record(new_record),
        "initial_prediction": pred_res
    }


def get_india_risk_summary() -> Dict[str, Any]:
    df = load_dataset()
    total_animals = len(df)
    
    no_risk = int((df["mastitis_risk_category"] == "No_Risk").sum())
    low_risk = int((df["mastitis_risk_category"] == "Low").sum())
    mod_risk = int((df["mastitis_risk_category"] == "Moderate").sum())
    high_risk = int((df["mastitis_risk_category"] == "High").sum())
    
    overall_avg_risk = round(float(df["synthetic_risk_score_pct"].mean()), 1)
    
    # State-wise aggregation
    state_data = {}
    if "state" in df.columns:
        for state_name, group in df.groupby("state"):
            s_total = len(group)
            s_no = int((group["mastitis_risk_category"] == "No_Risk").sum())
            s_low = int((group["mastitis_risk_category"] == "Low").sum())
            s_mod = int((group["mastitis_risk_category"] == "Moderate").sum())
            s_high = int((group["mastitis_risk_category"] == "High").sum())
            s_avg_risk = round(float(group["synthetic_risk_score_pct"].mean()), 1)
            
            # Risk level color tag
            if s_avg_risk < 25:
                risk_tier = "Low"
                color_hex = "#10b981" # Green
            elif s_avg_risk < 40:
                risk_tier = "Moderate"
                color_hex = "#f59e0b" # Yellow / Amber
            elif s_avg_risk < 60:
                risk_tier = "High"
                color_hex = "#f97316" # Orange
            else:
                risk_tier = "Critical"
                color_hex = "#ef4444" # Red
                
            state_data[state_name] = {
                "state": state_name,
                "total_animals": s_total,
                "no_risk": s_no,
                "low_risk": s_low,
                "moderate_risk": s_mod,
                "high_risk": s_high,
                "overall_risk_pct": s_avg_risk,
                "risk_tier": risk_tier,
                "color_hex": color_hex
            }
            
    return {
        "total_animals": total_animals,
        "no_risk_count": no_risk,
        "low_moderate_count": low_risk + mod_risk,
        "low_risk_count": low_risk,
        "moderate_risk_count": mod_risk,
        "high_risk_count": high_risk,
        "overall_herd_risk_pct": overall_avg_risk,
        "last_updated": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "state_risks": state_data
    }

def get_state_district_risk(state_name: str) -> Dict[str, Any]:
    df = load_dataset()
    if "state" not in df.columns:
        return {"error": "State column not found in dataset"}
        
    st_df = df[df["state"].str.lower() == state_name.lower().strip()]
    if st_df.empty:
        return {"state": state_name, "districts": [], "animals": []}
        
    actual_state_name = st_df.iloc[0]["state"]
    districts = []
    
    for dist_name, group in st_df.groupby("district"):
        d_total = len(group)
        d_high = int((group["mastitis_risk_category"] == "High").sum())
        d_mod = int((group["mastitis_risk_category"] == "Moderate").sum())
        d_low = int((group["mastitis_risk_category"] == "Low").sum())
        d_no = int((group["mastitis_risk_category"] == "No_Risk").sum())
        d_avg_risk = round(float(group["synthetic_risk_score_pct"].mean()), 1)
        
        if d_avg_risk < 25:
            d_tier = "Low"
        elif d_avg_risk < 40:
            d_tier = "Moderate"
        elif d_avg_risk < 60:
            d_tier = "High"
        else:
            d_tier = "Critical"
            
        districts.append({
            "district": dist_name,
            "total_animals": d_total,
            "high_risk_animals": d_high,
            "moderate_risk": d_mod,
            "low_risk": d_low,
            "no_risk": d_no,
            "risk_percentage": d_avg_risk,
            "risk_tier": d_tier
        })
        
    animals = [sanitize_record(r) for r in st_df.head(20).to_dict(orient="records")]
    
    return {
        "state": actual_state_name,
        "total_state_animals": len(st_df),
        "state_risk_pct": round(float(st_df["synthetic_risk_score_pct"].mean()), 1),
        "districts": districts,
        "animals_sample": animals
    }

def get_district_details(district_name: str) -> Dict[str, Any]:
    df = load_dataset()
    if "district" not in df.columns:
        return {"error": "District column not found in dataset"}
        
    d_df = df[df["district"].str.lower() == district_name.lower().strip()]
    if d_df.empty:
        return {"district": district_name, "farms": [], "animals": []}
        
    actual_dist_name = d_df.iloc[0]["district"]
    farms = []
    for farm_id, group in d_df.groupby("farm_id"):
        farms.append({
            "farm_id": farm_id,
            "total_animals": len(group),
            "high_risk_count": int((group["mastitis_risk_category"] == "High").sum()),
            "avg_risk": round(float(group["synthetic_risk_score_pct"].mean()), 1)
        })
        
    return {
        "district": actual_dist_name,
        "state": d_df.iloc[0]["state"],
        "total_animals": len(d_df),
        "district_risk_pct": round(float(d_df["synthetic_risk_score_pct"].mean()), 1),
        "farms": farms,
        "animals": [sanitize_record(r) for r in d_df.to_dict(orient="records")]
    }
