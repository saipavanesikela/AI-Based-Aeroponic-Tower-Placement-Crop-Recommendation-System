from fastapi import APIRouter, HTTPException
from app.services.ml_service import predict_crop_scores
from app.core.schemas import PredictionInput

router = APIRouter(
    prefix="/predict",
    tags=["Crop Suitability Prediction"]
)

@router.post("/")
def predict(input_data: PredictionInput):
    result = predict_crop_scores(
        input_data.temperature,
        input_data.humidity,
        input_data.wind_speed,
        input_data.sunlight_hours,
        input_data.x_coord,
        input_data.y_coord,
        input_data.spacing,
        input_data.shade_percent
    )
    # If prediction returned an error key, surface as HTTP 400
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result
