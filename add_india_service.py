# -*- coding: utf-8 -*-
with open("backend/app/services/data_service.py", "r", encoding="utf-8") as f:
    ds_code = f.read()

india_functions = """
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
"""

with open("backend/app/services/data_service.py", "w", encoding="utf-8") as f:
    f.write(ds_code + "\n" + india_functions)

print("Added get_india_risk_summary, get_state_district_risk, and get_district_details.")
