from fastapi import APIRouter
from app.services.ml_service import predict_crop_scores
from app.core.schemas import PredictionInput

router = APIRouter(
    prefix="/predict",
    tags=["Crop Suitability Prediction"]
)

@router.post("/")
def predict(input_data: PredictionInput):
    return predict_crop_scores(
        input_data.temperature,
        input_data.humidity,
        input_data.wind_speed,
        input_data.sunlight_hours,
        input_data.x_coord,
        input_data.y_coord,
        input_data.spacing,
        input_data.shade_percent
    )
