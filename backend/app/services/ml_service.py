# Crop-specific agronomic constraints
CROP_CONSTRAINTS = {
    "lettuce": {"temp": (15, 28), "hum": (60, 90), "sun": (4, 8)},
    "basil": {"temp": (22, 35), "hum": (50, 80), "sun": (6, 10)},
    "parsley": {"temp": (18, 30), "hum": (50, 80), "sun": (4, 8)},
    "mint": {"temp": (18, 30), "hum": (60, 90), "sun": (3, 7)},
    "rosemary": {"temp": (20, 32), "hum": (40, 70), "sun": (7, 12)}
}
import joblib
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# LOAD MODEL & ENCODER
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "placement_model.pkl"
ENCODER_PATH = BASE_DIR / "models" / "crop_encoder.pkl"

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

CROPS = ["lettuce", "basil", "parsley", "mint", "rosemary"]

# -------------------------------------------------
# INPUT VALIDATION
# -------------------------------------------------
def validate_inputs(
    temperature,
    humidity,
    wind_speed,
    sunlight_hours,
    spacing,
    shade_percent
):
    if not (0 <= temperature <= 50):
        return "Temperature must be between 0 and 50 °C"
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

# -------------------------------------------------
# EXTREME CONDITION HANDLING
# -------------------------------------------------
def is_impossible_condition(temperature, humidity):
    return temperature >= 45 and humidity >= 95

def extreme_condition_penalty(temperature, humidity, sunlight_hours):
    penalty = 1.0

    if temperature > 40:
        penalty *= 0.4
    if humidity > 90:
        penalty *= 0.6
    if sunlight_hours > 12:
        penalty *= 0.7

    return penalty

# -------------------------------------------------
# RULE-BASED EXPLANATION
# -------------------------------------------------
def generate_explanation(crop, temperature, humidity, sunlight_hours):
    reasons = []

    if crop == "lettuce":
        if temperature <= 28:
            reasons.append("Performs well in moderate temperatures")
        if humidity >= 60:
            reasons.append("Thrives in high humidity")
        if sunlight_hours <= 8:
            reasons.append("Prefers controlled sunlight")

    elif crop == "basil":
        if temperature >= 24:
            reasons.append("Grows best in warm temperatures")
        if sunlight_hours >= 6:
            reasons.append("Requires sufficient sunlight")

    elif crop == "parsley":
        if temperature <= 30:
            reasons.append("Adaptable to mild temperatures")
        if sunlight_hours <= 8:
            reasons.append("Tolerates partial sunlight")

    elif crop == "mint":
        if humidity >= 60:
            reasons.append("Favors humid environments")
        if sunlight_hours <= 7:
            reasons.append("Prefers indirect sunlight")

    elif crop == "rosemary":
        if sunlight_hours >= 7:
            reasons.append("Needs strong sunlight")
        if humidity <= 70:
            reasons.append("Prefers low to moderate humidity")

    return reasons or ["Suitable under given environmental conditions"]

# -------------------------------------------------
# MAIN PREDICTION FUNCTION
# -------------------------------------------------
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
    # Basic validation
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

    # Hard rejection for impossible environment
    if is_impossible_condition(temperature, humidity):
        return {
            "error": "Environmental conditions are unsuitable for aeroponic crop growth",
            "recommended_crops": [],
            "all_scores": []
        }

    results = []

    for crop in CROPS:
        crop_encoded = encoder.transform([crop])[0]

        for crop in CROPS:
            crop_encoded = encoder.transform([crop])[0]
            # Hard agronomic check
            c = CROP_CONSTRAINTS[crop]
            if not (c["temp"][0] <= temperature <= c["temp"][1] and c["hum"][0] <= humidity <= c["hum"][1] and c["sun"][0] <= sunlight_hours <= c["sun"][1]):
                prediction = 0
                final_confidence = 0.0
            else:
                input_df = pd.DataFrame([{
                    "crop_type": crop_encoded,
                    "temperature": temperature,
                    "humidity": humidity,
                    "sunlight_hours": sunlight_hours,
                    "wind_speed": wind_speed,
                    "x_coord": x_coord,
                    "y_coord": y_coord,
                    "spacing": spacing,
                    "shade_percent": shade_percent
                }])
                # Ensure column order matches training
                input_df = input_df[[
                    "crop_type",
                    "temperature",
                    "humidity",
                    "sunlight_hours",
                    "wind_speed",
                    "x_coord",
                    "y_coord",
                    "spacing",
                    "shade_percent"
                ]]
                # ML prediction
                prediction = model.predict(input_df)[0]
                probabilities = model.predict_proba(input_df)[0]
                raw_confidence = max(probabilities) * 100
                penalty = extreme_condition_penalty(
                    temperature, humidity, sunlight_hours
                )
                final_confidence = round(raw_confidence * penalty, 2)
            explanation = generate_explanation(
                crop, temperature, humidity, sunlight_hours
            )
            results.append({
                "crop": crop,
                "suitability_score": int(prediction),
                "confidence": final_confidence,
                "explanation": explanation
            })
    max_score = max(item["suitability_score"] for item in results)
    best_crops = [item for item in results if item["suitability_score"] == max_score]
    if best_crops:
        # Pick the one with highest confidence
        best_crop = max(best_crops, key=lambda x: x["confidence"])
        recommended = [best_crop["crop"]]
    else:
        recommended = []

    return {
        "all_scores": results,
        "recommended_crops": recommended
    }
