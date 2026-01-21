from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

router = APIRouter(prefix="/metrics", tags=["metrics"])
BASE = Path(__file__).resolve().parent.parent
MODELS = BASE / "models"
DATA = MODELS / "aeroponic_crop_suitability_dataset.csv"
MODEL_FILE = MODELS / "placement_model.pkl"
ENCODER_FILE = MODELS / "crop_encoder.pkl"
PLOT_FILE = MODELS / "data" / "class_distribution.png"


@router.get("/distribution")
def get_distribution_image():
    if not PLOT_FILE.exists():
        raise HTTPException(status_code=404, detail="Distribution image not found")
    return FileResponse(str(PLOT_FILE))


@router.get("/summary")
def get_metrics_summary():
    if not MODEL_FILE.exists() or not ENCODER_FILE.exists() or not DATA.exists():
        raise HTTPException(status_code=404, detail="Model, encoder or dataset missing")

    model = joblib.load(MODEL_FILE)
    encoder = joblib.load(ENCODER_FILE)
    df = pd.read_csv(DATA)
    if "suitability_class" not in df.columns:
        raise HTTPException(status_code=400, detail="Dataset missing suitability_class")

    X = df[["crop_type","temperature","humidity","sunlight_hours","water_ph","air_quality_index","wind_speed"]]
    # encode crop_type
    X["crop_type"] = encoder.transform(df["crop_type"])
    y = df["suitability_class"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    ypred = model.predict(Xte)

    acc = accuracy_score(yte, ypred)
    f1_w = f1_score(yte, ypred, average="weighted")
    report = classification_report(yte, ypred, zero_division=0, output_dict=True)
    cm = confusion_matrix(yte, ypred).tolist()

    return JSONResponse({
        "accuracy": acc,
        "weighted_f1": f1_w,
        "classification_report": report,
        "confusion_matrix": cm,
    })
