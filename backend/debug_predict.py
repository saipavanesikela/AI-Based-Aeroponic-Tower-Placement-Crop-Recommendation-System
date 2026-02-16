from app.models.crop_recommendation import get_model, get_calibrated_model, get_encoder, get_scaler
from app.core.config import CROPS, CROP_CONSTRAINTS, RECOMMENDATION_CONFIDENCE_THRESHOLD
import pandas as pd
import numpy as np

# Test input from your message
input_data = dict(
    temperature=30.0,
    humidity=90.0,
    sunlight_hours=8.8,
    water_ph=7.0,
    air_quality_index=90.0,
    wind_speed=5.0,
)

model = get_calibrated_model() or get_model()
encoder = get_encoder()
scaler = get_scaler()

print(f"Using model: {model}")
print(f"Encoder: {encoder}")
print(f"Scaler: {scaler}")

rows = []
for crop in CROPS:
    c = CROP_CONSTRAINTS.get(crop, {})
    crop_encoded = encoder.transform([crop])[0] if encoder is not None else 0
    df = pd.DataFrame([{
        "crop_type": crop_encoded,
        "temperature": input_data['temperature'],
        "humidity": input_data['humidity'],
        "sunlight_hours": input_data['sunlight_hours'],
        "water_ph": input_data['water_ph'],
        "air_quality_index": input_data['air_quality_index'],
        "wind_speed": input_data['wind_speed']
    }])
    df = df[["crop_type","temperature","humidity","sunlight_hours","water_ph","air_quality_index","wind_speed"]]

    if scaler is not None:
        X = scaler.transform(df)
    else:
        X = df.values

    try:
        raw_pred = model.predict(X)[0]
    except Exception as e:
        raw_pred = f"err:{e}"

    probs = None
    if hasattr(model, 'predict_proba'):
        try:
            probs = model.predict_proba(X)[0]
        except Exception as e:
            probs = f"err:{e}"

    raw_confidence = None
    if isinstance(probs, (list, tuple, np.ndarray)):
        raw_confidence = max(probs) * 100
    penalty = 1.0
    if input_data['temperature'] > 40:
        penalty *= 0.4
    if input_data['humidity'] > 90:
        penalty *= 0.6
    if input_data['sunlight_hours'] > 12:
        penalty *= 0.7
    if input_data['air_quality_index'] > 180:
        penalty *= 0.6

    final_confidence = round(raw_confidence * penalty, 2) if raw_confidence is not None else None

    try:
        raw_score = float(raw_pred)
    except Exception:
        raw_score = None
    suitability_score = int(np.clip(np.rint(raw_score), 0, 3)) if raw_score is not None else None

    rows.append({
        'crop': crop,
        'raw_pred': raw_pred,
        'probs': probs,
        'raw_confidence': raw_confidence,
        'penalty': penalty,
        'final_confidence': final_confidence,
        'suitability_score': suitability_score
    })

# Print detailed table
print('\nDetailed model outputs:')
for r in rows:
    print(r)

# Summarize any mismatches
print('\nMismatches (suitability_score vs final_confidence):')
for r in rows:
    sc = r['suitability_score']
    fc = r['final_confidence']
    if sc is not None and fc is not None:
        if (sc == 0 and fc > 50) or (sc >= 2 and fc < 50):
            print(f"Potential mismatch: {r['crop']} -> score={sc}, confidence={fc}")
