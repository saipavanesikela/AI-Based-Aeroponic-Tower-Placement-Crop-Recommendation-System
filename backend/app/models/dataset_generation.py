import random
from pathlib import Path
import pandas as pd

# -----------------------------
# Crop constraints (derived from literature)
# -----------------------------

CROPS = {
    "lettuce": {
        "temp": (15, 25),
        "humidity": (50, 80),
        "sunlight": (4, 6),
        "ph": (5.5, 6.5),
        "aqi_max": 120,
        "wind": (0.3, 1.5)
    },
    "basil": {
        "temp": (20, 30),
        "humidity": (50, 70),
        "sunlight": (6, 8),
        "ph": (5.5, 6.8),
        "aqi_max": 130,
        "wind": (0.3, 2.0)
    },
    "parsley": {
        "temp": (18, 25),
        "humidity": (50, 75),
        "sunlight": (4, 6),
        "ph": (5.5, 6.5),
        "aqi_max": 120,
        "wind": (0.3, 1.5)
    },
    "mint": {
        "temp": (18, 28),
        "humidity": (55, 80),
        "sunlight": (4, 6),
        "ph": (5.5, 6.5),
        "aqi_max": 125,
        "wind": (0.4, 2.0)
    },
    "rosemary": {
        "temp": (20, 30),
        "humidity": (40, 65),
        "sunlight": (6, 8),
        "ph": (6.0, 7.0),
        "aqi_max": 140,
        "wind": (0.5, 2.5)
    }
}

# -----------------------------
# Suitability scoring logic
# -----------------------------

def calculate_suitability(crop, temp, humidity, sunlight, ph, aqi, wind):
    score = 3  # start at ideal and deduct for any violation

    t_min, t_max = CROPS[crop]["temp"]
    h_min, h_max = CROPS[crop]["humidity"]
    s_min, s_max = CROPS[crop]["sunlight"]
    p_min, p_max = CROPS[crop]["ph"]
    aqi_max = CROPS[crop]["aqi_max"]
    w_min, w_max = CROPS[crop]["wind"]

    if not (t_min <= temp <= t_max):
        score -= 1
    if not (h_min <= humidity <= h_max):
        score -= 1
    if not (s_min <= sunlight <= s_max):
        score -= 1
    if not (p_min <= ph <= p_max):
        score -= 1
    if aqi > aqi_max:
        score -= 1
    if not (w_min <= wind <= w_max):
        score -= 1

    return max(score, 0)

# -----------------------------
# Dataset generation
# -----------------------------

def generate_dataset(samples_per_crop=200):
    rows = []

    for crop in CROPS:
        for _ in range(samples_per_crop):

            temperature = round(random.uniform(10, 40), 2)
            humidity = random.randint(30, 90)
            sunlight_hours = round(random.uniform(3, 9), 1)
            water_ph = round(random.uniform(5.0, 7.5), 2)
            air_quality_index = random.randint(30, 200)
            wind_speed = round(random.uniform(0.2, 3.0), 2)

            suitability_score = calculate_suitability(
                crop,
                temperature,
                humidity,
                sunlight_hours,
                water_ph,
                air_quality_index,
                wind_speed
            )

            rows.append({
                "crop_type": crop,
                "temperature": temperature,
                "humidity": humidity,
                "sunlight_hours": sunlight_hours,
                "water_ph": water_ph,
                "air_quality_index": air_quality_index,
                "wind_speed": wind_speed,
                "suitability_score": suitability_score
            })

    return pd.DataFrame(rows)

# -----------------------------
# Generate CSV
# -----------------------------

if __name__ == "__main__":
    df = generate_dataset(samples_per_crop=200)
    dataset_path = Path(__file__).resolve().parent / "aeroponic_crop_suitability_dataset.csv"
    df.to_csv(dataset_path, index=False)

    print("Dataset generated successfully!")
    print(df.head())
