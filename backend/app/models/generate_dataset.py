import pandas as pd
import random

NUM_ROWS = 1000

crop_constraints = {
    "lettuce": {"temp": (15, 25), "hum": (60, 80), "sun": (4, 6)},
    "basil": {"temp": (20, 30), "hum": (50, 70), "sun": (6, 8)},
    "parsley": {"temp": (18, 28), "hum": (60, 80), "sun": (4, 6)},
    "mint": {"temp": (18, 30), "hum": (60, 85), "sun": (4, 6)},
    "rosemary": {"temp": (20, 30), "hum": (40, 60), "sun": (6, 8)}
}

rows = []

for _ in range(NUM_ROWS):
    crop = random.choice(list(crop_constraints.keys()))
    c = crop_constraints[crop]

    temperature = round(random.uniform(15, 35), 1)
    humidity = round(random.uniform(40, 90), 1)
    wind_speed = round(random.uniform(0.5, 6), 1)
    sunlight = round(random.uniform(1, 9), 1)

    x = random.randint(1, 10)
    y = random.randint(1, 10)
    spacing = round(random.uniform(0.4, 1.6), 2)
    shade = random.randint(0, 50)

    # Yield scoring
    if (c["temp"][0] <= temperature <= c["temp"][1] and
        c["hum"][0] <= humidity <= c["hum"][1] and
        c["sun"][0] <= sunlight <= c["sun"][1] and
        shade <= 20):
        yield_score = 4
    elif sunlight >= c["sun"][0] and shade <= 30:
        yield_score = 3
    elif sunlight >= 3:
        yield_score = 2
    else:
        yield_score = 1

    rows.append([
        crop, temperature, humidity, wind_speed, sunlight,
        x, y, spacing, shade, yield_score
    ])

df = pd.DataFrame(rows, columns=[
    "crop_type", "temperature", "humidity", "wind_speed",
    "sunlight_hours", "x_coord", "y_coord",
    "spacing", "shade_percent", "yield_score"
])

df.to_csv("aeroponic_crop_placement_dataset.csv", index=False)
print("Dataset created successfully!")
