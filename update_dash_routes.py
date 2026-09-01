# -*- coding: utf-8 -*-
with open("backend/app/routes/dashboard.py", "w", encoding="utf-8") as f:
    f.write("""from fastapi import APIRouter
from app.services.data_service import (
    get_dashboard_summary,
    get_india_risk_summary,
    get_state_district_risk,
    get_district_details
)

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    return get_dashboard_summary()

@router.get("/dashboard/india-risk")
def get_india_risk():
    return get_india_risk_summary()

@router.get("/dashboard/state/{state_name}")
def get_state_risk(state_name: str):
    return get_state_district_risk(state_name)

@router.get("/dashboard/district/{district_name}")
def get_district_risk(district_name: str):
    return get_district_details(district_name)
""")

print("Updated backend/app/routes/dashboard.py with India map endpoints.")
