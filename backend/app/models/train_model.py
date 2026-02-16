from pathlib import Path
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from sklearn.neural_network import MLPClassifier

BASE = Path(__file__).parent
csv_v2 = BASE / "aeroponic_crop_suitability_dataset_v2.csv"
csv_default = BASE / "aeroponic_crop_suitability_dataset.csv"
if csv_v2.exists():
    df = pd.read_csv(csv_v2)
    print(f"Using dataset: {csv_v2.name}")
else:
    df = pd.read_csv(csv_default)
    print(f"Using dataset: {csv_default.name}")

# Support datasets that name the label column 'suitability_class'
if "suitability_score" not in df.columns and "suitability_class" in df.columns:
    df = df.rename(columns={"suitability_class": "suitability_score"})

le = LabelEncoder()
df["crop_type"] = le.fit_transform(df["crop_type"])

FEATURE_COLS = [
    "crop_type", "temperature", "humidity", "sunlight_hours",
    "water_ph", "air_quality_index", "wind_speed"
]

X = df[FEATURE_COLS]
y = df["suitability_score"]

Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

def evaluate_model(y_true, y_pred):
    return {
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted")),
        "accuracy": float(accuracy_score(y_true, y_pred))
    }

# Final ANN training configuration requested by user
# Ensure dataset is exactly 1500 rows (sample if larger) and train final ANN with 1000 iterations
TARGET_DATASET_SIZE = 1500
if len(df) > TARGET_DATASET_SIZE:
    print(f"Dataset has {len(df)} rows; sampling down to {TARGET_DATASET_SIZE} for final training")
    df = df.sample(n=TARGET_DATASET_SIZE, random_state=42)
elif len(df) < TARGET_DATASET_SIZE:
    print(f"Warning: dataset has only {len(df)} rows; expected {TARGET_DATASET_SIZE}. Proceeding with available rows.")

size = len(df)

# Rebuild X/y and train-test split after any sampling
X = df[FEATURE_COLS]
y = df["suitability_score"]

Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(Xtr)
X_test_scaled = scaler.transform(Xte)

# Train final ANN
FINAL_ITER = 1000
ann = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=FINAL_ITER, random_state=42)
print(f"Training final ANN on {size} rows with max_iter={FINAL_ITER}...")
ann.fit(X_train_scaled, ytr)
preds = ann.predict(X_test_scaled)

metrics = evaluate_model(yte, preds)
metrics.update({
    "model": "ANN_final",
    "dataset_size": size,
    "iterations": FINAL_ITER
})

print(f"Final ANN -> f1_weighted={metrics['f1_weighted']:.4f}, accuracy={metrics['accuracy']:.4f}")

# Save final model and artifacts
joblib.dump(ann, BASE / "placement_model.pkl")
joblib.dump(le, BASE / "crop_encoder.pkl")
joblib.dump(scaler, BASE / "feature_scaler.pkl")
print(f"Saved final ANN model to {BASE / 'placement_model.pkl'} and encoder/scaler to models directory")

# Save results
pd.DataFrame([metrics]).to_csv(BASE / "training_results_ann_final.csv", index=False)
print(f"Wrote final training results to {BASE / 'training_results_ann_final.csv'}")