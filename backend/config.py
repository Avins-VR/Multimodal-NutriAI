import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Central configuration for the Flask backend.
    All values are read from environment variables.
    """

    # ── Groq API ──
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    GROQ_MODEL = "openai/gpt-oss-20b"

    # ── CORS ──
    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173"
    ).split(",")

    # ── Model / data paths ──
    MODEL_PATH = os.getenv(
        "MODEL_PATH",
        "ml_models/image_model.pth"
    )

    RF_MODEL_PATH = os.getenv(
        "RF_MODEL_PATH",
        "ml_models/rf_metadata_model.pkl"
    )

    SCALER_PATH = os.getenv(
        "SCALER_PATH",
        "ml_models/rf_scaler.pkl"
    )

    DATA_PATH = os.getenv(
        "DATA_PATH",
        "data/train_data.csv"
    )

    # ── Google Drive file ID for the image model ──
    MODEL_DRIVE_FILE_ID = os.getenv(
        "MODEL_DRIVE_FILE_ID",
        "1QQuBf5gwGVR36Bn3HanBU5H5gGbaYznA"
    )

    # ── Flask ──
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"