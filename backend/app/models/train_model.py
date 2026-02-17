from pathlib import Path
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
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

# Accept datasets that name the label column 'suitability_class' or 'suitability_score'
if "suitability_score" not in df.columns and "suitability_class" in df.columns:
    df = df.rename(columns={"suitability_class": "suitability_score"})

# Target dataset size used in Colab experiments
TARGET_DATASET_SIZE = 1500
if len(df) > TARGET_DATASET_SIZE:
    print(f"Dataset has {len(df)} rows; sampling down to {TARGET_DATASET_SIZE} for final training")
    df = df.sample(n=TARGET_DATASET_SIZE, random_state=42)
elif len(df) < TARGET_DATASET_SIZE:
    print(f"Warning: dataset has only {len(df)} rows; expected {TARGET_DATASET_SIZE}. Proceeding with available rows.")

le = LabelEncoder()
if df['crop_type'].dtype == object:
    df['crop_type'] = le.fit_transform(df['crop_type'])
else:
    le.fit(df['crop_type'])

FEATURE_COLS = [
    "crop_type", "temperature", "humidity", "sunlight_hours",
    "water_ph", "air_quality_index", "wind_speed"
]

X = df[FEATURE_COLS]
y = df["suitability_score"]

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(Xtr)
X_test_scaled = scaler.transform(Xte)

def evaluate(y_true, y_pred):
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision_weighted": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    }

# Colab ANN configuration (adjusted): 200 iterations, hidden layers (64,32)
FINAL_ITER = 200
ann = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=FINAL_ITER, random_state=42)
print(f"Training ANN (hidden=(64,32), max_iter={FINAL_ITER}) on {len(df)} rows...")
ann.fit(X_train_scaled, ytr)
preds = ann.predict(X_test_scaled)

metrics = evaluate(yte, preds)
metrics.update({"model": "ANN_colab_style", "dataset_size": len(df), "iterations": FINAL_ITER})

print(f"Training results: accuracy={metrics['accuracy']:.4f}, f1_weighted={metrics['f1_weighted']:.4f}")
print("Classification report:\n")
print(classification_report(yte, preds, zero_division=0))

# Save artifacts
joblib.dump(ann, BASE / "placement_model.pkl")
joblib.dump(le, BASE / "crop_encoder.pkl")
joblib.dump(scaler, BASE / "feature_scaler.pkl")
print(f"Saved model and artifacts to {BASE}")

# Persist results
pd.DataFrame([metrics]).to_csv(BASE / "training_results_ann_final.csv", index=False)
print(f"Wrote training results to {BASE / 'training_results_ann_final.csv'}")