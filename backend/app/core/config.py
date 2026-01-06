
# Centralized configuration file

APP_NAME = "Aeroponic Tower Placement System"
VERSION = "1.0"

# Crop constraints and list
CROP_CONSTRAINTS = {
	"lettuce": {"temp": (15, 28), "hum": (60, 90), "sun": (4, 8)},
	"basil": {"temp": (22, 35), "hum": (50, 80), "sun": (6, 10)},
	"parsley": {"temp": (18, 30), "hum": (50, 80), "sun": (4, 8)},
	"mint": {"temp": (18, 30), "hum": (60, 90), "sun": (3, 7)},
	"rosemary": {"temp": (20, 32), "hum": (40, 70), "sun": (7, 12)}
}
CROPS = list(CROP_CONSTRAINTS.keys())

# Model paths
import pathlib
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "placement_model.pkl"
ENCODER_PATH = BASE_DIR / "models" / "crop_encoder.pkl"
