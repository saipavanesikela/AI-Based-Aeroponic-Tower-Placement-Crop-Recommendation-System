import logging
from typing import List

import numpy as np
import pandas as pd
from pathlib import Path

from app.core.config import CROP_CONSTRAINTS, CROPS, RECOMMENDATION_CONFIDENCE_THRESHOLD
from app.models.crop_recommendation import (
    get_model,
    get_calibrated_model,
    get_encoder,
    get_scaler,
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

    if is_impossible_condition(temperature, humidity, air_quality_index):
        return {"error": "Environmental conditions are unsuitable for aeroponic crop growth", "recommended_crops": [], "all_scores": []}

    results: List[dict] = []

    # Load dataset summary for per-crop empirical suitability (if available).
    # This helps smooth model overconfidence by incorporating historical suitability percentages.
    try:
        dataset_path = Path(__file__).resolve().parents[1] / "models" / "aeroponic_crop_suitability_dataset_v2.csv"
        if dataset_path.exists():
            ds = pd.read_csv(dataset_path)
            # compute mean suitability percentage per crop
            crop_mean_pct = ds.groupby("crop_type")["suitability_percentage"].mean().to_dict()
        else:
            crop_mean_pct = {}
    except Exception:
        crop_mean_pct = {}

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

        # If a scaler is available (e.g., ANN trained on scaled features), apply it
        scaler = get_scaler()
        if scaler is not None:
            try:
                X_input = scaler.transform(input_df)
            except Exception:
                X_input = input_df.values
        else:
            X_input = input_df.values

        # Get model output; support classifiers (with predict_proba) and regressors
        try:
            raw_pred = model.predict(X_input)[0]
        except Exception:
            raw_pred = 0

        # Probabilities: only available for classifiers
        if hasattr(model, "predict_proba"):
            try:
                probabilities = model.predict_proba(X_input)[0]
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

        # Empirical dataset confidence for this crop (0..1)
        data_conf = float(crop_mean_pct.get(crop, np.nan)) / 100.0 if crop_mean_pct else np.nan
        # Normalize model probability to 0..1
        model_prob = float(raw_confidence) / 100.0 if raw_confidence is not None else 0.0

        # Combine model probability and empirical dataset confidence to reduce
        # overconfident predictions. Weigh model higher but keep dataset as stabilizer.
        if not np.isnan(data_conf):
            combined_confidence_base = (0.6 * model_prob) + (0.4 * data_conf)
        else:
            combined_confidence_base = model_prob

        final_confidence = round(combined_confidence_base * penalty * 100, 2)

        # Interpret raw_pred: if model is regressor, raw_pred may be continuous; clip/round to 0..3
        try:
            raw_score = float(raw_pred)
        except Exception:
            raw_score = 0.0

        # Compute a combined suitability score that blends the model raw score
        # with dataset-derived empirical suitability. This helps when the model
        # outputs low-granularity classes but dataset shows stronger tendencies.
        try:
            max_class = 3.0
            model_score_norm = float(raw_score) / max_class if max_class > 0 else 0.0
        except Exception:
            model_score_norm = 0.0

        if not np.isnan(data_conf):
            combined_score_norm = (0.6 * model_score_norm) + (0.4 * data_conf)
        else:
            combined_score_norm = model_score_norm

        suitability_score = int(np.clip(np.rint(combined_score_norm * 3.0), 0, 3))

        # Include model-predicted suitability for visibility (do not zero it out)
        prediction = suitability_score
        agronomic_flag = bool(agronomic_ok)

        # Compute agronomic violations (soft constraints): count how many
        # constraint checks failed so we can apply a softer penalty instead
        # of hard-excluding crops when dataset/model indicate suitability.
        violations = 0
        if not (c.get("temp", (0, 999))[0] <= temperature <= c.get("temp", (0, 999))[1]):
            violations += 1
        if not (c.get("hum", (0, 999))[0] <= humidity <= c.get("hum", (0, 999))[1]):
            violations += 1
        if not (c.get("sun", (0, 999))[0] <= sunlight_hours <= c.get("sun", (0, 999))[1]):
            violations += 1
        if not (c.get("ph", (0, 999))[0] <= water_ph <= c.get("ph", (0, 999))[1]):
            violations += 1
        if not (c.get("wind", (0, 999))[0] <= wind_speed <= c.get("wind", (0, 999))[1]):
            violations += 1

        # Agronomic penalty factor: each violation reduces confidence mildly
        agronomic_penalty_factor = (0.88 ** violations) if violations > 0 else 1.0

        # Apply agronomic penalty to the previously computed final_confidence
        final_confidence = round(final_confidence * agronomic_penalty_factor, 2)

        # Include raw model score for visibility
        model_raw = round(raw_score, 3)

        explanation = generate_explanation(crop, temperature, humidity, sunlight_hours, water_ph, air_quality_index, wind_speed)
        results.append({
            "crop": crop,
            "suitability_score": int(prediction),
            "model_raw_score": model_raw,
            "confidence": final_confidence,
            "agronomic_ok": agronomic_flag,
            "explanation": explanation,
        })

    # Prefer agronomically-eligible crops, but fall back to best overall when
    # none are eligible. This improves UX after dataset/model changes.
    eligible = [r for r in results if r.get("agronomic_ok")]
    recommended = []
    candidates = eligible if eligible else results

    if candidates:
        best = max(candidates, key=lambda x: (x.get("confidence", 0), x.get("suitability_score", 0)))
        if best.get("confidence", 0) >= RECOMMENDATION_CONFIDENCE_THRESHOLD:
            recommended = [best["crop"]]
        else:
            recommended = []

    return {"all_scores": results, "recommended_crops": recommended}
