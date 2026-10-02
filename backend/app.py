"""
Multimodal NutriAI — Flask backend.

Only the UI technology changed from the original Streamlit app: this
Flask API reproduces the exact same ML + chatbot logic behind three
routes (plus a health check) that the React frontend calls.

    React frontend
          |
          v
    POST /api/predict, POST /api/chat
          |
          v
    Flask API  (this file)
          |
          v
    ML models / Mistral API

Run with:
    python app.py
or:
    flask run
"""

import logging

import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image

from config import Config
from services import chatbot_service, image_service, metadata_service, recommendation_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nutriai-backend")

app = Flask(__name__)
CORS(app, origins=Config.ALLOWED_ORIGINS)


def init_models() -> None:
    """
    Loads every model / dataset exactly once, at application startup —
    never inside a request handler.
    """
    logger.info("Loading image model (downloading if necessary)...")
    image_service.load_image_model(Config.MODEL_PATH, Config.MODEL_DRIVE_FILE_ID)

    logger.info("Loading Random Forest metadata model + scaler...")
    metadata_service.load_metadata_model(Config.RF_MODEL_PATH, Config.SCALER_PATH)

    logger.info("Loading recommendation training data...")
    recommendation_service.load_recommendation_data(Config.DATA_PATH)

    logger.info("All models loaded. Backend ready.")


init_models()


# ================================
# HEALTH CHECK
# ================================
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        {"success": True, "service": "Multimodal NutriAI API", "status": "running"}
    )


# ================================
# PREDICTION
# ================================
@app.route("/api/predict", methods=["POST"])
def predict():
    # ── Validate image ──
    if "image" not in request.files or request.files["image"].filename == "":
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Please upload a leaf image before running the analysis.",
                }
            ),
            400,
        )

    image_file = request.files["image"]

    try:
        image = Image.open(image_file.stream).convert("RGB")
    except Exception:
        return jsonify({"success": False, "error": "Invalid image file."}), 400

    # ── Validate metadata ──
    try:
        metadata = {
            key: float(request.form.get(key))
            for key in metadata_service.features
        }
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Invalid metadata values."}), 400

    # ── Run the original prediction pipeline ──
    try:
        img_prob = image_service.image_prediction(image)
        meta_prob = metadata_service.metadata_prediction(metadata)
        final_prob = metadata_service.fusion(img_prob, meta_prob)

        predicted = int(np.argmax(final_prob))
        label = metadata_service.class_names[predicted]
        confidence = float(np.max(final_prob) * 100)

        recommendation = recommendation_service.get_recommendation(metadata, label)

        probabilities = {
            cls: float(final_prob[i] * 100)
            for i, cls in enumerate(metadata_service.class_names)
        }

        return jsonify(
            {
                "success": True,
                "prediction": label,
                "confidence": confidence,
                "probabilities": probabilities,
                "recommendation": recommendation,
            }
        )
    except Exception:
        logger.exception("Prediction failed")
        return jsonify({"success": False, "error": "Prediction failed."}), 500


# ================================
# CHAT
# ================================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages")

    if not messages or not isinstance(messages, list):
        return jsonify({"success": False, "error": "Chatbot request failed."}), 400

    try:
        reply = chatbot_service.get_agriculture_response(messages)
        return jsonify({"success": True, "response": reply})
    except Exception:
        logger.exception("Chat request failed")
        return jsonify({"success": False, "error": "Chatbot request failed."}), 500


# ================================
# AGRICULTURE TOPIC CLASSIFIER (optional helper endpoint)
# ================================
@app.route("/api/chat/check-topic", methods=["POST"])
def check_topic():
    data = request.get_json(silent=True) or {}
    question = data.get("question")

    if not question:
        return jsonify({"success": False, "error": "No question provided."}), 400

    is_agriculture = chatbot_service.check_agriculture(question)
    return jsonify({"is_agriculture": is_agriculture})


if __name__ == "__main__":
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
