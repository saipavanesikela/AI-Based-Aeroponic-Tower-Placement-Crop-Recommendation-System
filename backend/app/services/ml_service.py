import logging
from typing import List

import numpy as np
import pandas as pd

from app.core.config import CROP_CONSTRAINTS, CROPS, RECOMMENDATION_CONFIDENCE_THRESHOLD
from app.models.crop_recommendation import (
    get_model,
    get_calibrated_model,
    get_encoder,
    is_model_available,
)

logger = logging.getLogger("ml_service")


def validate_inputs(temperature, humidity, sunlight_hours, water_ph, air_quality_index, wind_speed):
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


def validate_and_gate_inputs(temperature, water_ph, air_quality_index):
    """
    Hard safety rules that run before ML prediction. If any rule fails,
    the inputs are immediately rejected as UNSUITABLE (class 0).

    Rules:
    - temperature > 40 or temperature < 10 -> UNSUITABLE
    - water_ph < 4.8 or water_ph > 7.2 -> UNSUITABLE
    - air_quality_index > 180 -> UNSUITABLE

    Returns: (passes: bool, reason: str)
    """
    if temperature > 40 or temperature < 10:
        return False, "Temperature outside safe bounds"
    if water_ph < 4.8 or water_ph > 7.2:
        return False, "Water pH outside safe bounds"
    if air_quality_index > 180:
        return False, "Air Quality Index too high"
    return True, "OK"


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


def generate_explanation(crop, temperature, humidity, sunlight_hours, water_ph, air_quality_index, wind_speed):
    reasons = []
    c = CROP_CONSTRAINTS.get(crop, {})
    if temperature <= c.get("temp", (0, 999))[1]:
        reasons.append("Temperature within preferred range")
    if humidity >= c.get("hum", (0, 0))[0]:
        reasons.append("Humidity within preferred range")
    reasons.append(f"pH input: {water_ph}")
    reasons.append(f"AQI input: {air_quality_index}")
    return reasons


def predict_crop_scores(
    temperature: float,
    humidity: float,
    sunlight_hours: float,
    water_ph: float,
    air_quality_index: float,
    wind_speed: float,
) -> dict:
    if not is_model_available():
        return {"error": "Model artifacts not available. Run training or place model/encoder .pkl files in backend/app/models"}

    # prefer calibrated model for better probability estimates
    model = get_calibrated_model() or get_model()
    encoder = get_encoder()

    # validate
    error = validate_inputs(temperature, humidity, sunlight_hours, water_ph, air_quality_index, wind_speed)
    if error:
        return {"error": error, "recommended_crops": [], "all_scores": []}

    # Hard-rule gating before any ML work
    passes, reason = validate_and_gate_inputs(temperature, water_ph, air_quality_index)
    if not passes:
        # Return a rule-based rejection for all crops
        results = []
        for crop in CROPS:
            results.append({
                "crop": crop,
                "suitability_class": 0,
                "model_raw_score": None,
                "confidence": 100.0,
                "agronomic_ok": False,
                "explanation": ["Rule-based rejection: " + reason],
            })
        return {"all_scores": results, "recommended_crops": [], "rule_rejection": True}

    if is_impossible_condition(temperature, humidity, air_quality_index):
        return {"error": "Environmental conditions are unsuitable for aeroponic crop growth", "recommended_crops": [], "all_scores": []}

    results: List[dict] = []

    for crop in CROPS:
        c = CROP_CONSTRAINTS.get(crop, {})
        # strict agronomic checks (except AQI handled softly)
        agronomic_ok = (
            c.get("temp", (0, 999))[0] <= temperature <= c.get("temp", (0, 999))[1]
            and c.get("hum", (0, 999))[0] <= humidity <= c.get("hum", (0, 999))[1]
            and c.get("sun", (0, 999))[0] <= sunlight_hours <= c.get("sun", (0, 999))[1]
            and c.get("ph", (0, 999))[0] <= water_ph <= c.get("ph", (0, 999))[1]
            and c.get("wind", (0, 999))[0] <= wind_speed <= c.get("wind", (0, 999))[1]
        )

        # Always compute model prediction/probabilities so we can return confidence for all crops
        crop_encoded = encoder.transform([crop])[0] if encoder is not None else 0
        input_df = pd.DataFrame([{"crop_type": crop_encoded, "temperature": temperature, "humidity": humidity, "sunlight_hours": sunlight_hours, "water_ph": water_ph, "air_quality_index": air_quality_index, "wind_speed": wind_speed}])
        input_df = input_df[["crop_type", "temperature", "humidity", "sunlight_hours", "water_ph", "air_quality_index", "wind_speed"]]

        # Get model output; support classifiers (with predict_proba) and regressors
        try:
            raw_pred = model.predict(input_df)[0]
        except Exception:
            raw_pred = 0

        # Probabilities: only available for classifiers
        if hasattr(model, "predict_proba"):
            try:
                probabilities = model.predict_proba(input_df)[0]
            except Exception:
                probabilities = [0.0]
        else:
            probabilities = [0.0]

        raw_confidence = max(probabilities) * 100 if len(probabilities) > 0 else 0.0
        penalty = extreme_condition_penalty(temperature, humidity, sunlight_hours, air_quality_index)

        crop_aqi_max = c.get("aqi") or c.get("aqi_max")
        if crop_aqi_max is not None and air_quality_index > crop_aqi_max:
            excess = air_quality_index - crop_aqi_max
            scale = max(20.0, float(crop_aqi_max))
            aqi_penalty = max(0.1, 1.0 - (excess / scale))
            penalty *= aqi_penalty

        final_confidence = round(raw_confidence * penalty, 2)

        # Interpret raw_pred: if model is regressor, raw_pred may be continuous; clip/round to 0..3
        try:
            raw_score = float(raw_pred)
        except Exception:
            raw_score = 0.0

        # Map model output to 3-class range [0,2]
        suitability_class = int(np.clip(np.rint(raw_score), 0, 2))
        prediction = suitability_class
        agronomic_flag = bool(agronomic_ok)

        # Include raw model score for visibility
        model_raw = round(raw_score, 3)

        explanation = generate_explanation(crop, temperature, humidity, sunlight_hours, water_ph, air_quality_index, wind_speed)
        results.append({
            "crop": crop,
            "suitability_class": int(prediction),
            "model_raw_score": model_raw,
            "confidence": final_confidence,
            "agronomic_ok": agronomic_flag,
            "explanation": explanation,
        })

    # Only consider agronomically-eligible crops for recommendations
    eligible = [r for r in results if r.get("agronomic_ok")]
    recommended = []
    if eligible:
        max_score = max(item["suitability_class"] for item in eligible)
        best_crops = [item for item in eligible if item["suitability_class"] == max_score]
        if best_crops:
            best_crop = max(best_crops, key=lambda x: x.get("confidence", 0))
            if best_crop.get("confidence", 0) >= RECOMMENDATION_CONFIDENCE_THRESHOLD:
                recommended = [best_crop["crop"]]

    return {"all_scores": results, "recommended_crops": recommended}
