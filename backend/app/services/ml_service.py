import joblib
import pandas as pd
from pathlib import Path

# Get base directory: backend/app/
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "placement_model.pkl"
ENCODER_PATH = BASE_DIR / "models" / "crop_encoder.pkl"

# Load trained model and encoder
model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

CROPS = ["lettuce", "basil", "parsley", "mint", "rosemary"]
def validate_inputs(
    temperature,
    humidity,
    wind_speed,
    sunlight_hours,
    spacing,
    shade_percent
):
    if not (0 <= temperature <= 45):
        return "Temperature must be between 0 and 45 °C"

    if not (20 <= humidity <= 100):
        return "Humidity must be between 20% and 100%"

    if not (0 <= wind_speed <= 10):
        return "Wind speed must be between 0 and 10 m/s"

    if not (0 <= sunlight_hours <= 24):
        return "Sunlight hours must be between 0 and 24"

    if not (0.5 <= spacing <= 5.0):
        return "Spacing must be between 0.5 and 5 meters"

    if not (0 <= shade_percent <= 100):
        return "Shade percent must be between 0 and 100"

    return None

def predict_crop_scores(
    temperature,
    humidity,
    wind_speed,
    sunlight_hours,
    x_coord,
    y_coord,
    spacing,
    shade_percent
):
    error = validate_inputs(
        temperature,
        humidity,
        wind_speed,
        sunlight_hours,
        spacing,
        shade_percent
    )

    if error:
        return {
            "error": error,
            "recommended_crops": [],
            "all_scores": []
        }

    results = []


    for crop in CROPS:
        encoded_crop = encoder.transform([crop])[0]

        input_df = pd.DataFrame([{
            "crop_type": encoded_crop,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "sunlight_hours": sunlight_hours,
            "x_coord": x_coord,
            "y_coord": y_coord,
            "spacing": spacing,
            "shade_percent": shade_percent
        }])

        score = int(model.predict(input_df)[0])

        results.append({
            "crop": crop,
            "suitability_score": score
        })

    max_score = max(item["suitability_score"] for item in results)
    recommended = [
        item["crop"] for item in results
        if item["suitability_score"] == max_score
    ]

    return {
        "all_scores": results,
        "recommended_crops": recommended
    }
