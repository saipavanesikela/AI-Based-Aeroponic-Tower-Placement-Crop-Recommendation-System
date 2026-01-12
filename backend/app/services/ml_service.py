from app.core.config import CROP_CONSTRAINTS, CROPS, MODEL_PATH, ENCODER_PATH
import joblib
import pandas as pd
import logging
from app.models.crop_recommendation import get_model, get_encoder, is_model_available

logger = logging.getLogger("ml_service")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    logger.exception("Failed to load model: %s", e)
    model = None

try:
    encoder = joblib.load(ENCODER_PATH)
except Exception as e:
    logger.exception("Failed to load encoder: %s", e)
    encoder = None

# -------------------------------------------------
# INPUT VALIDATION
# -------------------------------------------------
def validate_inputs(
    temperature,
    humidity,
    sunlight_hours,
    water_ph,
    air_quality_index,
    wind_speed
):
    if not (0 <= temperature <= 50):
        return "Temperature must be between 0 and 50 °C"
    if not (20 <= humidity <= 100):
        return "Humidity must be between 20% and 100%"
    if not (0 <= sunlight_hours <= 24):
        return "Sunlight hours must be between 0 and 24"
    if not (4.5 <= water_ph <= 8.0):
        return "Water pH must be between 4.5 and 8.0"
    if not (0 <= air_quality_index <= 500):
        return "Air Quality Index must be between 0 and 500"
    if not (0 <= wind_speed <= 5.0):
        return "Wind speed must be between 0 and 5 m/s"
    return None

# -------------------------------------------------
# EXTREME CONDITION HANDLING
# -------------------------------------------------
def is_impossible_condition(temperature, humidity, aqi):
    return (temperature >= 45 and humidity >= 95) or aqi >= 400

def extreme_condition_penalty(temperature, humidity, sunlight_hours, air_quality_index):
    penalty = 1.0

    if temperature > 40:
        penalty *= 0.4
    if humidity > 90:
        penalty *= 0.6
    if sunlight_hours > 12:
        penalty *= 0.7
    if air_quality_index > 180:
        penalty *= 0.6

    return penalty

# -------------------------------------------------
# RULE-BASED EXPLANATION
# -------------------------------------------------
def generate_explanation(crop, temperature, humidity, sunlight_hours, water_ph, air_quality_index, wind_speed):
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
    if water_ph:
        reasons.append(f"pH input: {water_ph}")
    if air_quality_index:
        reasons.append(f"AQI input: {air_quality_index}")
    if wind_speed:
        reasons.append(f"Wind input: {wind_speed}")

    return reasons or ["Suitable under given environmental conditions"]

# -------------------------------------------------
# MAIN PREDICTION FUNCTION
# -------------------------------------------------
def predict_crop_scores(
    temperature,
    humidity,
    sunlight_hours,
    water_ph,
    air_quality_index,
    wind_speed
):
    if not is_model_available():
        return {"error": "Model artifacts not available. Run training or place model/encoder .pkl files in backend/app/models"}

    model = get_model()
    encoder = get_encoder()

    logger.info(
        "Predict called with: temp=%s hum=%s sun=%s ph=%s aqi=%s wind=%s",
        temperature,
        humidity,
        sunlight_hours,
        water_ph,
        air_quality_index,
        wind_speed,
    )

    # Basic validation
    error = validate_inputs(
        temperature,
        humidity,
        sunlight_hours,
        water_ph,
        air_quality_index,
        wind_speed
    )

    if error:
        logger.warning("Validation failed: %s", error)
        return {
            "error": error,
            "recommended_crops": [],
            "all_scores": []
        }

    # Hard rejection for impossible environment
    if is_impossible_condition(temperature, humidity, air_quality_index):
        return {
            "error": "Environmental conditions are unsuitable for aeroponic crop growth",
            "recommended_crops": [],
            "all_scores": []
        }

    results = []

    for crop in CROPS:
        # Hard agronomic check
        c = CROP_CONSTRAINTS[crop]
        if not (
            c["temp"][0] <= temperature <= c["temp"][1]
            and c["hum"][0] <= humidity <= c["hum"][1]
            and c["sun"][0] <= sunlight_hours <= c["sun"][1]
            and c["ph"][0] <= water_ph <= c["ph"][1]
            and air_quality_index <= c["aqi"]
            and c["wind"][0] <= wind_speed <= c["wind"][1]
        ):
            prediction = 0
            final_confidence = 0.0
        else:
            # encode crop if encoder available
            crop_encoded = encoder.transform([crop])[0] if encoder is not None else 0
            input_df = pd.DataFrame([{
                "crop_type": crop_encoded,
                "temperature": temperature,
                "humidity": humidity,
                "sunlight_hours": sunlight_hours,
                "water_ph": water_ph,
                "air_quality_index": air_quality_index,
                "wind_speed": wind_speed
            }])
            # Ensure column order matches training
            input_df = input_df[[
                "crop_type",
                "temperature",
                "humidity",
                "sunlight_hours",
                "water_ph",
                "air_quality_index",
                "wind_speed"
            ]]
            # ML prediction
            if model is None or encoder is None:
                prediction = 0
                probabilities = [0.0] * len(getattr(model, "classes_", [0]))
            else:
                prediction = model.predict(input_df)[0]
                probabilities = model.predict_proba(input_df)[0]
            raw_confidence = max(probabilities) * 100
            penalty = extreme_condition_penalty(
                temperature, humidity, sunlight_hours, air_quality_index
            )
            final_confidence = round(raw_confidence * penalty, 2)
        explanation = generate_explanation(
            crop, temperature, humidity, sunlight_hours, water_ph, air_quality_index, wind_speed
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

    result = {
        "all_scores": results,
        "recommended_crops": recommended
    }
    logger.info("Prediction result: %s crops=%d", "ok", len(results))
    return result
