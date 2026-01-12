import joblib
import pandas as pd


from app.core.config import CROPS, MODEL_PATH, ENCODER_PATH

_model = None
_encoder = None

try:
    _model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: failed to load model from {MODEL_PATH}: {e}")

try:
    _encoder = joblib.load(ENCODER_PATH)
except Exception as e:
    print(f"Warning: failed to load encoder from {ENCODER_PATH}: {e}")

def get_model():
    return _model

def get_encoder():
    return _encoder

def is_model_available():
    return _model is not None and _encoder is not None

crops = CROPS

if __name__ == "__main__":
    # Example usage (runs only when executed directly)
    if not is_model_available():
        print("Model or encoder not available. Run training or place model/encoder .pkl files in backend/app/models")
    else:
        user_input = {
            "temperature": 26,
            "humidity": 65,
            "sunlight_hours": 7,
            "water_ph": 6.2,
            "air_quality_index": 80,
            "wind_speed": 1.2
        }

        results = []

        for crop in crops:
            try:
                encoder = get_encoder()
                model = get_model()
                encoded_crop = encoder.transform([crop])[0]
                data = pd.DataFrame([{
                    "crop_type": encoded_crop,
                    **user_input
                }])
                score = model.predict(data)[0]
                results.append((crop, score))
            except Exception as e:
                print(f"Skipping crop {crop} due to error: {e}")

        if results:
            results_df = pd.DataFrame(results, columns=["Crop", "Suitability_Score"])
            print(results_df)
            max_score = results_df["Suitability_Score"].max()
            best_crops = results_df[results_df["Suitability_Score"] == max_score]
            print("\nRecommended Crops (Best Suitable):")
            print(best_crops)
        else:
            print("No results available")
