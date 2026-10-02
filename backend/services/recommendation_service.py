"""
Recommendation service.

Reproduces, unchanged, the original Streamlit application's
get_recommendation() logic:
  1. Filter train_data.csv rows to the predicted class.
  2. Scale those rows' features with the same fitted scaler.
  3. Scale the current input metadata.
  4. Compute Euclidean distance from the input to every filtered row.
  5. Take the 5 nearest rows.
  6. Randomly select one of those 5 recommendations.

Loaded once at application startup (see app.py) and reused for every request.
"""

import numpy as np
import pandas as pd

from services.metadata_service import features, get_scaler

# Module-level holder populated by load_recommendation_data().
_data_df = None


def load_recommendation_data(data_path: str) -> pd.DataFrame:
    """
    Loads train_data.csv once and caches it at module level.
    """
    global _data_df
    _data_df = pd.read_csv(data_path)
    return _data_df


def get_recommendation(metadata_dict: dict, predicted_class: str) -> str:
    """
    Returns one recommendation string, randomly chosen among the 5 nearest
    training rows (by Euclidean distance in scaled feature space) that
    share the predicted class — exactly the original logic.
    """
    if _data_df is None:
        raise RuntimeError("Recommendation data has not been loaded yet.")

    scaler = get_scaler()

    class_data = _data_df[_data_df["Label"] == predicted_class]
    X = scaler.transform(class_data[features])
    y = class_data["Recommendation"].values

    input_scaled = scaler.transform(pd.DataFrame([metadata_dict])[features])
    dist = np.linalg.norm(X - input_scaled, axis=1)

    idx = np.random.choice(np.argsort(dist)[:5])
    return y[idx]
