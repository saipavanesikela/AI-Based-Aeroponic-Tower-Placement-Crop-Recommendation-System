import random
from pathlib import Path
import pandas as pd

# -------------------------------
# Crop configuration (unchanged)
# -------------------------------
CROPS = {
    "lettuce":  {"temp": (15, 25), "humidity": (50, 80), "sunlight": (4, 6), "ph": (5.5, 6.5), "aqi": 120, "wind": (0.3, 1.5)},
    "basil":    {"temp": (20, 30), "humidity": (50, 70), "sunlight": (6, 8), "ph": (5.5, 6.8), "aqi": 130, "wind": (0.3, 2.0)},
    "parsley":  {"temp": (18, 25), "humidity": (50, 75), "sunlight": (4, 6), "ph": (5.5, 6.5), "aqi": 120, "wind": (0.3, 1.5)},
    "mint":     {"temp": (18, 28), "humidity": (55, 80), "sunlight": (4, 6), "ph": (5.5, 6.5), "aqi": 125, "wind": (0.4, 2.0)},
    "rosemary": {"temp": (20, 30), "humidity": (40, 65), "sunlight": (6, 8), "ph": (6.0, 7.0), "aqi": 140, "wind": (0.5, 2.5)},
}

# -------------------------------
# Smooth scoring (DL-friendly)
# -------------------------------
def smooth_score(value, low, high, weight):
    center = (low + high) / 2
    max_dist = (high - low) / 2

    dist = abs(value - center)
    score = weight * max(0, 1 - (dist / (max_dist * 2)))
    return score


def calculate_percentage(crop, t, h, s, ph, aqi, w):
    cfg = CROPS[crop]
    score = 0

    score += smooth_score(ph, *cfg["ph"], 20)
    score += smooth_score(t, *cfg["temp"], 20)
    score += smooth_score(h, *cfg["humidity"], 15)
    score += smooth_score(s, *cfg["sunlight"], 15)
    score += smooth_score(w, *cfg["wind"], 10)

    # AQI: lower is better
    aqi_score = max(0, 20 * (1 - aqi / cfg["aqi"]))
    score += aqi_score

    return round(min(score, 100), 2)


def percentage_to_class_3way(pct):
    if pct >= 70:
        return 2
    elif pct >= 45:
        return 1
    return 0


# -------------------------------
# Correlated sampling
# -------------------------------
def sample_environment(cfg, mode="ideal"):
    t_center = sum(cfg["temp"]) / 2

    if mode == "ideal":
        t = random.gauss(t_center, 1.5)
    elif mode == "borderline":
        t = random.gauss(t_center + random.choice([-4, 4]), 2.5)
    else:
        t = random.uniform(5, 50)

    # Correlations
    h = random.gauss(sum(cfg["humidity"]) / 2 - 0.3 * (t - t_center), 6)
    aqi = int(random.gauss(45 + 0.6 * abs(t - t_center), 15))

    s = random.gauss(sum(cfg["sunlight"]) / 2, 0.8)
    ph = random.gauss(sum(cfg["ph"]) / 2, 0.25)
    w = random.gauss(sum(cfg["wind"]) / 2, 0.35)

    # Clamp values
    t = round(max(-10, min(55, t)), 2)
    h = int(max(0, min(100, h)))
    s = round(max(0, min(24, s)), 1)
    ph = round(max(3.0, min(9.0, ph)), 2)
    aqi = int(max(0, min(500, aqi)))
    w = round(max(0, min(10, w)), 2)

    return t, h, s, ph, aqi, w


# -------------------------------
# Dataset generation
# -------------------------------
def generate(samples_per_crop=300):
    rows = []
    modes = ["ideal", "borderline", "poor"]
    probs = [0.4, 0.3, 0.3]

    for crop, cfg in CROPS.items():
        for _ in range(samples_per_crop):
            mode = random.choices(modes, probs)[0]
            t, h, s, ph, aqi, w = sample_environment(cfg, mode)

            pct = calculate_percentage(crop, t, h, s, ph, aqi, w)
            cls = percentage_to_class_3way(pct)

            rows.append({
                "crop_type": crop,
                "temperature": t,
                "humidity": h,
                "sunlight_hours": s,
                "water_ph": ph,
                "air_quality_index": aqi,
                "wind_speed": w,
                "suitability_percentage": pct,
                "suitability_class": cls,
            })

    return pd.DataFrame(rows)


# -------------------------------
# Run & save
# -------------------------------
if __name__ == "__main__":
    df = generate()
    out = Path(__file__).parent / "aeroponic_crop_suitability_dataset_v2.csv"
    df.to_csv(out, index=False)
    print("Improved dataset generated:", out)
