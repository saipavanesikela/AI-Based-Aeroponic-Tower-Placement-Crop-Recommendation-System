import pandas as pd
import random


from app.core.config import CROP_CONSTRAINTS, CROPS
SEASONS = ["summer", "monsoon", "winter"]

def add_noise(value, percent=5):
    return round(value + value * random.uniform(-percent, percent) / 100, 2)

def seasonal_adjustment(season):
    if season == "summer":
        return -10, +1
    if season == "monsoon":
        return +10, -1
    return 0, 0

def calculate_yield_score(temp, hum, sun, c):
    # Strict: if any variable is out of range, score is 0
    if not (c["temp"][0] <= temp <= c["temp"][1]):
        return 0
    if not (c["hum"][0] <= hum <= c["hum"][1]):
        return 0
    if not (c["sun"][0] <= sun <= c["sun"][1]):
        return 0
    return 3

def is_valid(row):
    return (
        0 <= row["temperature"] <= 45 and
        20 <= row["humidity"] <= 100 and
        0 <= row["sunlight_hours"] <= 24 and
        0 <= row["wind_speed"] <= 10 and
        0.5 <= row["spacing"] <= 5.0 and
        0 <= row["shade_percent"] <= 100 and
        0 <= row["x_coord"] <= 100 and
        0 <= row["y_coord"] <= 100
    )

data = []

for _ in range(1500):
    crop = random.choice(CROPS)
    c = CROP_CONSTRAINTS[crop]

    temp = random.uniform(*c["temp"])
    hum = add_noise(random.uniform(*c["hum"]))
    sun = add_noise(random.uniform(*c["sun"]))
    wind_speed = round(random.uniform(0, 10), 2)
    x_coord = random.randint(0, 100)
    y_coord = random.randint(0, 100)
    spacing = round(random.uniform(0.5, 5.0), 2)
    shade_percent = round(random.uniform(0, 100), 2)

    yield_score = calculate_yield_score(temp, hum, sun, c)

    row = {
        "crop_type": crop,
        "temperature": round(temp, 2),
        "humidity": round(hum, 2),
        "sunlight_hours": round(sun, 2),
        "wind_speed": wind_speed,
        "x_coord": x_coord,
        "y_coord": y_coord,
        "spacing": spacing,
        "shade_percent": shade_percent,
        "yield_score": yield_score
    }
    if is_valid(row):
        data.append([
            row["crop_type"],
            row["temperature"],
            row["humidity"],
            row["sunlight_hours"],
            row["wind_speed"],
            row["x_coord"],
            row["y_coord"],
            row["spacing"],
            row["shade_percent"],
            row["yield_score"]
        ])

df = pd.DataFrame(
    data,
    columns=[
        "crop_type",
        "temperature",
        "humidity",
        "sunlight_hours",
        "wind_speed",
        "x_coord",
        "y_coord",
        "spacing",
        "shade_percent",
        "yield_score"
    ]
)

df.to_csv("aeroponic_crop_placement_dataset_realistic.csv", index=False)
print("Realistic dataset generated!")
