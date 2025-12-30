import joblib
import pandas as pd

# Load trained model and encoder
model = joblib.load("placement_model.pkl")
encoder = joblib.load("crop_encoder.pkl")

# Crops considered
crops = ["lettuce", "basil", "parsley", "mint", "rosemary"]

# -------- USER INPUT (example) --------
user_input = {
    "temperature": 26,
    "humidity": 65,
    "wind_speed": 2.5,
    "sunlight_hours": 7,
    "x_coord": 5,
    "y_coord": 5,
    "spacing": 1.2,
    "shade_percent": 15
}

results = []

for crop in crops:
    encoded_crop = encoder.transform([crop])[0]

    data = pd.DataFrame([{
        "crop_type": encoded_crop,
        **user_input
    }])

    score = model.predict(data)[0]

    results.append((crop, score))

# Display results
results_df = pd.DataFrame(results, columns=["Crop", "Suitability_Score"])


# Find max score
max_score = results_df["Suitability_Score"].max()

# All best crops
best_crops = results_df[
    results_df["Suitability_Score"] == max_score
]

print(results_df)
print("\nRecommended Crops (Best Suitable):")
print(best_crops)
