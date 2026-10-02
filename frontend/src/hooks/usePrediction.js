import { useState } from "react";
import { runPrediction } from "../services/api.js";

/**
 * Encapsulates prediction state + the call to the backend.
 *
 * Returns:
 *  - predictionResult: { prediction, confidence, probabilities, recommendation } | null
 *  - isPredicting: boolean
 *  - predictionError: string | null
 *  - predict: (file: File, soilData: object) => Promise<void>
 *  - reset: () => void
 */
export default function usePrediction() {
  const [predictionResult, setPredictionResult] = useState(null);
  const [isPredicting, setIsPredicting] = useState(false);
  const [predictionError, setPredictionError] = useState(null);

  const predict = async (file, soilData) => {
    setIsPredicting(true);
    setPredictionError(null);

    try {
      const formData = new FormData();
      formData.append("image", file);
      Object.entries(soilData).forEach(([key, value]) => {
        formData.append(key, value);
      });

      const result = await runPrediction(formData);
      setPredictionResult(result);
    } catch (err) {
      setPredictionError(err.message || "Something went wrong during analysis.");
      setPredictionResult(null);
    } finally {
      setIsPredicting(false);
    }
  };

  const reset = () => {
    setPredictionResult(null);
    setPredictionError(null);
  };

  return { predictionResult, isPredicting, predictionError, predict, reset };
}
