# Centralized configuration file

APP_NAME = "Aeroponic Tower Placement System"
VERSION = "1.0"

# Crop constraints and list
CROP_CONSTRAINTS = {
	"lettuce": {"temp": (15, 25), "hum": (50, 80), "sun": (4, 6), "ph": (5.5, 6.5), "aqi": 120, "wind": (0.3, 1.5)},
	"basil": {"temp": (20, 30), "hum": (50, 70), "sun": (6, 8), "ph": (5.5, 6.8), "aqi": 130, "wind": (0.3, 2.0)},
	"parsley": {"temp": (18, 25), "hum": (50, 75), "sun": (4, 6), "ph": (5.5, 6.5), "aqi": 120, "wind": (0.3, 1.5)},
	"mint": {"temp": (18, 28), "hum": (55, 80), "sun": (4, 6), "ph": (5.5, 6.5), "aqi": 125, "wind": (0.4, 2.0)},
	"rosemary": {"temp": (20, 30), "hum": (40, 65), "sun": (6, 8), "ph": (6.0, 7.0), "aqi": 140, "wind": (0.5, 2.5)}
}
CROPS = list(CROP_CONSTRAINTS.keys())

# Model paths
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent  # backend/app
MODELS_DIR = BASE_DIR / "models"

# Update these names to match your saved artifacts
MODEL_PATH = MODELS_DIR / "placement_model.pkl"
ENCODER_PATH = MODELS_DIR / "crop_encoder.pkl"

# Calibrated model (optional). If present, API will prefer this for calibrated probabilities
CALIBRATED_MODEL_PATH = MODELS_DIR / "placement_model_calibrated.pkl"

# Minimum confidence (%) required to include a crop in `recommended_crops`
RECOMMENDATION_CONFIDENCE_THRESHOLD = 74
