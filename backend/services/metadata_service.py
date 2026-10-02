"""
Metadata model service.

Reproduces, unchanged, the original Streamlit application's:
  - class_names / features constants
  - Random Forest metadata_prediction() function (with class reordering)
  - fusion() function (0.7 image / 0.3 metadata)

Loaded once at application startup (see app.py) and reused for every request.
"""

import joblib
import numpy as np
import pandas as pd

class_names = ["Healthy", "Early Deficiency", "Critical Deficiency"]

features = [
    "N",
    "P",
    "K",
    "ph",
    "soil_moisture",
    "temperature",
    "humidity",
    "rainfall",
    "sunlight_exposure",
]

# Module-level holders populated by load_metadata_model().
_rf_model = None
_scaler = None
_rf_classes = None


def load_metadata_model(rf_model_path: str, scaler_path: str):
    """
    Loads the Random Forest classifier and its fitted scaler once, and
    caches them at module level.
    """
    global _rf_model, _scaler, _rf_classes

    _rf_model = joblib.load(rf_model_path)
    _scaler = joblib.load(scaler_path)
    _rf_classes = _rf_model.classes_

    return _rf_model, _scaler


def get_scaler():
    if _scaler is None:
        raise RuntimeError("Scaler has not been loaded yet.")
    return _scaler


def metadata_prediction(metadata_dict: dict) -> np.ndarray:
    """
    Runs the Random Forest prediction and reorders its output probabilities
    to match class_names — exactly the original reordering logic, since the
    Random Forest's own class order (rf_model.classes_) is not assumed to
    already match class_names.
    """
    if _rf_model is None or _scaler is None:
        raise RuntimeError("Metadata model has not been loaded yet.")

    df = pd.DataFrame([metadata_dict])
    scaled = _scaler.transform(df[features])
    probs = _rf_model.predict_proba(scaled)[0]

    ordered = np.zeros(len(class_names))
    for i, cls in enumerate(_rf_classes):
        idx = class_names.index(cls)
        ordered[idx] = probs[i]

    return ordered


def fusion(img_prob: np.ndarray, meta_prob: np.ndarray) -> np.ndarray:
    """
    Multimodal fusion — MUST remain 70% image / 30% metadata.
    """
    return 0.7 * img_prob + 0.3 * meta_prob
