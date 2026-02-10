import random
from pathlib import Path
import pandas as pd

CROPS = {
    "lettuce":  {"temp": (15,25), "humidity": (50,80), "sunlight": (4,6), "ph": (5.5,6.5), "aqi":120, "wind":(0.3,1.5)},
    "basil":    {"temp": (20,30), "humidity": (50,70), "sunlight": (6,8), "ph": (5.5,6.8), "aqi":130, "wind":(0.3,2.0)},
    "parsley":  {"temp": (18,25), "humidity": (50,75), "sunlight": (4,6), "ph": (5.5,6.5), "aqi":120, "wind":(0.3,1.5)},
    "mint":     {"temp": (18,28), "humidity": (55,80), "sunlight": (4,6), "ph": (5.5,6.5), "aqi":125, "wind":(0.4,2.0)},
    "rosemary": {"temp": (20,30), "humidity": (40,65), "sunlight": (6,8), "ph": (6.0,7.0), "aqi":140, "wind":(0.5,2.5)}
}

def percentage_to_class(p):
    if p >= 85: return 4
    if p >= 70: return 3
    if p >= 55: return 2
    if p >= 40: return 1
    return 0

def calculate_percentage(crop, t, h, s, ph, aqi, w):
    cfg = CROPS[crop]
    score = 100

    if not cfg["ph"][0] <= ph <= cfg["ph"][1]: score -= 25
    if not cfg["temp"][0] <= t <= cfg["temp"][1]: score -= 20
    if not cfg["humidity"][0] <= h <= cfg["humidity"][1]: score -= 15
    if aqi > cfg["aqi"]: score -= 15
    if not cfg["sunlight"][0] <= s <= cfg["sunlight"][1]: score -= 10
    if not cfg["wind"][0] <= w <= cfg["wind"][1]: score -= 10

    return max(score, 0)

def generate(samples=250):
    rows = []

    for crop, cfg in CROPS.items():
        for _ in range(samples):
            t  = random.gauss(sum(cfg["temp"])/2, 3)
            h  = random.gauss(sum(cfg["humidity"])/2, 10)
            s  = random.uniform(cfg["sunlight"][0]-1, cfg["sunlight"][1]+1)
            ph = random.gauss(sum(cfg["ph"])/2, 0.3)
            aqi = random.gauss(80, 30)
            w  = random.gauss(sum(cfg["wind"])/2, 0.4)

            p = calculate_percentage(crop, t, h, s, ph, aqi, w)

            rows.append({
                "crop_type": crop,
                "temperature": round(t,2),
                "humidity": int(max(30,min(90,h))),
                "sunlight_hours": round(s,1),
                "water_ph": round(max(5,min(7.5,ph)),2),
                "air_quality_index": int(max(30,min(200,aqi))),
                "wind_speed": round(max(0.2,min(3.0,w)),2),
                "suitability_percentage": p,
                "suitability_score": percentage_to_class(p)
            })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate()
    out = Path(__file__).parent / "aeroponic_crop_suitability_dataset.csv"
    df.to_csv(out, index=False)
    print("Dataset generated:", out)
