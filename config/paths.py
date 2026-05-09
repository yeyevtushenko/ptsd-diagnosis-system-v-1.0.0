from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

FEATURE_CONFIG_PATH = CONFIG_DIR / "feature_config.json"
SELECTED_FEATURES_PATH = MODELS_DIR / "selected_features.json"
MODEL_METADATA_PATH = MODELS_DIR / "model_metadata.json"
MODEL_COEFFICIENTS_PATH = MODELS_DIR / "model_coefficients.json"