from pathlib import Path
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

BASE = Path(__file__).parent
df = pd.read_csv(BASE / "aeroponic_crop_suitability_dataset.csv")

le = LabelEncoder()
df["crop_type"] = le.fit_transform(df["crop_type"])

X = df[
    ["crop_type","temperature","humidity","sunlight_hours",
     "water_ph","air_quality_index","wind_speed"]
]
y = df["suitability_score"]

Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = RandomForestClassifier(
    n_estimators=400,
    max_depth=14,
    min_samples_leaf=3,
    class_weight="balanced",
    n_jobs=-1,
    random_state=42
)

model.fit(Xtr, ytr)
pred = model.predict(Xte)

print("Weighted F1:", f1_score(yte, pred, average="weighted"))

joblib.dump(model, BASE / "placement_model.pkl")
joblib.dump(le, BASE / "crop_encoder.pkl")
