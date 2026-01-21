from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


BASE = Path(__file__).parent


def load_data():
    df = pd.read_csv(BASE / "aeroponic_crop_suitability_dataset.csv")
    return df


def prepare_features(df, encoder):
    df = df.copy()
    # match the same column name used during training
    df["crop_type"] = encoder.transform(df["crop_type"])
    X = df[["crop_type", "temperature", "humidity", "sunlight_hours", "water_ph", "air_quality_index", "wind_speed"]]
    y = df["suitability_class"]
    return X, y


def evaluate():
    # Load artifacts
    model = joblib.load(BASE / "placement_model.pkl")
    encoder = joblib.load(BASE / "crop_encoder.pkl")

    # Load and prepare data
    df = load_data()
    X, y = prepare_features(df, encoder)

    # Use same split as training for a comparable test set
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # Predict and compute metrics
    ypred = model.predict(Xte)

    acc = accuracy_score(yte, ypred)
    f1_w = f1_score(yte, ypred, average="weighted")
    prec_w = precision_score(yte, ypred, average="weighted", zero_division=0)
    rec_w = recall_score(yte, ypred, average="weighted", zero_division=0)

    print("Evaluation results on hold-out test set:")
    print(f"  Accuracy: {acc:.4f}")
    print(f"  Weighted F1: {f1_w:.4f}")
    print(f"  Weighted Precision: {prec_w:.4f}")
    print(f"  Weighted Recall: {rec_w:.4f}")
    print("\nClassification report:")
    print(classification_report(yte, ypred, zero_division=0))
    print("Confusion matrix:")
    print(confusion_matrix(yte, ypred))


if __name__ == "__main__":
    evaluate()
