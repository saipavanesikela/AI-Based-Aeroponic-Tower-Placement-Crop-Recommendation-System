 
import random
from pathlib import Path
import pandas as pd


CROPS = {
    "lettuce":  {"temp": (15, 25), "humidity": (50, 80), "sunlight": (4, 6), "ph": (5.5, 6.5), "aqi": 120, "wind": (0.3, 1.5)},
    "basil":    {"temp": (20, 30), "humidity": (50, 70), "sunlight": (6, 8), "ph": (5.5, 6.8), "aqi": 130, "wind": (0.3, 2.0)},
    "parsley":  {"temp": (18, 25), "humidity": (50, 75), "sunlight": (4, 6), "ph": (5.5, 6.5), "aqi": 120, "wind": (0.3, 1.5)},
    "mint":     {"temp": (18, 28), "humidity": (55, 80), "sunlight": (4, 6), "ph": (5.5, 6.5), "aqi": 125, "wind": (0.4, 2.0)},
    "rosemary": {"temp": (20, 30), "humidity": (40, 65), "sunlight": (6, 8), "ph": (6.0, 7.0), "aqi": 140, "wind": (0.5, 2.5)},
}


def percentage_to_class_3way(pct: float) -> int:
    if pct >= 75:
        return 2
    if pct >= 55:
        return 1
    return 0


def calculate_percentage(crop, t, h, s, ph, aqi, w):
    cfg = CROPS[crop]
    score = 100
    if not cfg["ph"][0] <= ph <= cfg["ph"][1]:
        score -= 25
    if not cfg["temp"][0] <= t <= cfg["temp"][1]:
        score -= 20
    if not cfg["humidity"][0] <= h <= cfg["humidity"][1]:
        score -= 15
    if aqi > cfg["aqi"]:
        score -= 15
    if not cfg["sunlight"][0] <= s <= cfg["sunlight"][1]:
        score -= 10
    if not cfg["wind"][0] <= w <= cfg["wind"][1]:
        score -= 10
    return max(score, 0)


def sample_ideal(cfg):
    mean_temp = sum(cfg["temp"]) / 2
    t = random.gauss(mean_temp, 2)
    h = random.gauss(sum(cfg["humidity"]) / 2, 5)
    s = random.gauss(sum(cfg["sunlight"]) / 2, 0.5)
    ph = random.gauss(sum(cfg["ph"]) / 2, 0.15)
    aqi = max(10, int(random.gauss(50, 15)))
    w = random.gauss(sum(cfg["wind"]) / 2, 0.2)
    return t, h, s, ph, aqi, w


def sample_borderline(cfg):
    low_t, high_t = cfg["temp"]
    if random.random() < 0.5:
        t = random.gauss(low_t - 2, 2.5)
    else:
        t = random.gauss(high_t + 2, 2.5)
    low_h, high_h = cfg["humidity"]
    if random.random() < 0.5:
        h = random.gauss(max(10, low_h - 10), 8)
    else:
        h = random.gauss(min(100, high_h + 10), 8)
    s = random.gauss(sum(cfg["sunlight"]) / 2, 1.2)
    ph = random.gauss(sum(cfg["ph"]) / 2 + (0.3 if random.random() < 0.5 else -0.3), 0.3)
    aqi = max(20, int(random.gauss(80, 25)))
    w = random.gauss(sum(cfg["wind"]) / 2, 0.4)
    return t, h, s, ph, aqi, w


def sample_poor(cfg):
    if random.random() < 0.5:
        t = random.uniform(5.0, 11.5)
    else:
        t = random.uniform(38.5, 50.0)
    if random.random() < 0.5:
        ph = random.uniform(3.5, 4.9)
    else:
        ph = random.uniform(7.3, 9.0)
    aqi = int(random.uniform(151, 400))
    if random.random() < 0.5:
        h = random.uniform(5.0, 29.9)
    else:
        h = random.uniform(90.0, 100.0)
    s = random.gauss(sum(cfg["sunlight"]) / 2, 2.0)
    w = random.gauss(sum(cfg["wind"]) / 2, 0.6)
    return t, h, s, ph, aqi, w


def generate(samples_per_crop=800, ideal_pct=0.35, borderline_pct=0.30, poor_pct=0.35):
    """
    Generate a synthetic dataset using conditional sampling with configurable mode ratios.
    Defaults increase `poor` sampling to 35% and larger sample size per crop.
    """
    rows = []
    mode_probs = [("ideal", ideal_pct), ("borderline", borderline_pct), ("poor", poor_pct)]
    for crop, cfg in CROPS.items():
        for _ in range(samples_per_crop):
            r = random.random()
            if r < mode_probs[0][1]:
                t, h, s, ph, aqi, w = sample_ideal(cfg)
            elif r < mode_probs[0][1] + mode_probs[1][1]:
                t, h, s, ph, aqi, w = sample_borderline(cfg)
            else:
                t, h, s, ph, aqi, w = sample_poor(cfg)
            t = round(max(-10.0, min(55.0, t)), 2)
            h = int(max(0, min(100, h)))
            s = round(max(0.0, min(24.0, s)), 1)
            ph = round(max(3.0, min(9.0, ph)), 2)
            aqi = int(max(0, min(500, aqi)))
            w = round(max(0.0, min(10.0, w)), 2)
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
    df = pd.DataFrame(rows)
    counts = df["suitability_class"].value_counts()
    if not counts.empty:
        min_count = int(counts.min())
        balanced = pd.concat([
            df[df["suitability_class"] == c].sample(n=min_count, random_state=42)
            for c in sorted(df["suitability_class"].unique())
        ], ignore_index=True)
    else:
        balanced = df
    return balanced


if __name__ == "__main__":
    df = generate()
    out = Path(__file__).parent / "aeroponic_crop_suitability_dataset.csv"
    df.to_csv(out, index=False)
    print("Dataset generated:", out)

