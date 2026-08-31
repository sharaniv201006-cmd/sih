# -*- coding: utf-8 -*-
with open("backend/app/services/data_service.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace get_sensor_data_by_id with realistic physiological progression
old_sensor_func = """def get_sensor_data_by_id(animal_id: int) -> Optional[Dict[str, Any]]:
    df = load_dataset()
    matched = df[df["animal_id"] == animal_id]
    if matched.empty:
        return None

    row = sanitize_record(matched.iloc[0].to_dict())
    
    base_body_temp = float(row.get("body_temperature_c", 38.6) or 38.6)
    base_udder_temp = float(row.get("udder_surface_temperature_c", 33.9) or 33.9)
    base_cond = float(row.get("milk_conductivity_mS_cm", 4.2) or 4.2)
    base_yield = float(row.get("milk_yield_kg_day", 15.0) or 15.0)
    base_amb_temp = float(row.get("ambient_temperature_c", 28.0) or 28.0)
    base_rel_hum = float(row.get("relative_humidity_pct", 70.0) or 70.0)

    telemetry_points = []
    days = ["Day -6", "Day -5", "Day -4", "Day -3", "Day -2", "Day -1", "Today"]
    
    for i, day in enumerate(days):
        delta = (i - 6) * 0.05
        telemetry_points.append({
            "day": day,
            "body_temperature_c": round(base_body_temp + delta * 0.4 + (i % 2) * 0.05, 2),
            "udder_surface_temperature_c": round(base_udder_temp + delta * 0.3 + (i % 3) * 0.04, 2),
            "milk_conductivity_mS_cm": round(max(3.0, base_cond + delta * 0.3), 2),
            "milk_yield_kg_day": round(max(5.0, base_yield - delta * 0.8), 2),
            "ambient_temperature_c": round(base_amb_temp + (i % 3 - 1) * 0.6, 1),
            "relative_humidity_pct": round(base_rel_hum + (i % 2 - 0.5) * 2.0, 1),
            "hygiene_score": round(float(row.get("hygiene_score_0_100", 60.0) or 60.0), 1)
        })

    return {
        "animal_id": animal_id,
        "current_telemetry": row,
        "telemetry_trend": telemetry_points
    }"""

new_sensor_func = """def get_sensor_data_by_id(animal_id: int) -> Optional[Dict[str, Any]]:
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
    }"""

if old_sensor_func in code:
    code = code.replace(old_sensor_func, new_sensor_func)
    with open("backend/app/services/data_service.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("data_service.py updated with dynamic telemetry trends.")
else:
    print("Function pattern not matched, rewriting file...")
