from app.services.ml_service import predict_crop_scores
import json
r = predict_crop_scores(temperature=30.0, humidity=90.0, sunlight_hours=8.8, water_ph=7.0, air_quality_index=90.0, wind_speed=5.0)
print(json.dumps(r, indent=2))
