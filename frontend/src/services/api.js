// ================================
// API SERVICE
// ================================
// All requests go through the Flask backend. The React frontend never
// talks to the Mistral API or the ML models directly — see architecture
// note in the README.
//
// React frontend → Flask API → ML models / Mistral API

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api";

/**
 * Runs the leaf-deficiency prediction.
 *
 * Expects the backend to accept a multipart/form-data payload containing:
 *  - image: File
 *  - soil parameters (N, P, K, ph, soil_moisture, temperature, humidity,
 *    rainfall, sunlight_exposure) as individual fields
 *
 * Expected response shape:
 * {
 *   "prediction": "Healthy",
 *   "confidence": 92.5,
 *   "probabilities": {
 *     "Healthy": 92.5,
 *     "Early Deficiency": 5.2,
 *     "Critical Deficiency": 2.3
 *   },
 *   "recommendation": "..."
 * }
 *
 * @param {FormData} formData
 * @returns {Promise<object>}
 */
export async function runPrediction(formData) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.error || `Prediction failed (${response.status})`);
  }

  return response.json();
}

/**
 * Sends the current chat history to the backend and returns the
 * assistant's reply. The Flask backend is responsible for the
 * agriculture-only scoping and the Mistral API call.
 *
 * @param {Array<{role: "user" | "assistant", content: string}>} messages
 * @returns {Promise<string>} the assistant's reply text
 */
export async function sendChatMessage(messages) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages })
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.error || `Chat request failed (${response.status})`);
  }

  const data = await response.json();
  return data.response;
}
