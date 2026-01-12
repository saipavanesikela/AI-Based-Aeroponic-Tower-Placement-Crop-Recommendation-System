from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "aeroponic_crop_suitability_dataset.csv"

# Load dataset generated from the new constraints
df = pd.read_csv(DATASET_PATH)

# Encode crop_type so the classifier can ingest it
le = LabelEncoder()
df["crop_type"] = le.fit_transform(df["crop_type"])

# Features now match the regenerated dataset
feature_cols = [
    "crop_type",
    "temperature",
    "humidity",
    "sunlight_hours",
    "water_ph",
    "air_quality_index",
    "wind_speed"
]
X = df[feature_cols]
y = df["suitability_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Slightly deeper forest with more trees for better accuracy without heavy cost
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(f"Weighted F1-Score: {f1 * 100:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# Persist artifacts for the API (kept names for compatibility)
joblib.dump(model, BASE_DIR / "placement_model.pkl")
joblib.dump(le, BASE_DIR / "crop_encoder.pkl")

print("Model and encoder saved successfully")
