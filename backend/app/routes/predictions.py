from fastapi import APIRouter, HTTPException
from app.schemas import PredictionInput, PredictionResponse
from app.ml.predict import predict_single_animal
from app.services.data_service import get_animal_detail

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_mastitis_risk(payload: PredictionInput):
    data_dict = payload.model_dump()
    result = predict_single_animal(data_dict)
    return result

@router.get("/predictions/{animal_id}")
def get_animal_prediction(animal_id: int):
    detail = get_animal_detail(animal_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Animal {animal_id} not found.")
    return detail["prediction"]
