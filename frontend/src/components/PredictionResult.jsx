import React from "react";
import DiagnosisCard from "./DiagnosisCard.jsx";
import RecommendationCard from "./RecommendationCard.jsx";

/**
 * Props:
 *  - imagePreview: string | null
 *  - predictionResult: { prediction, confidence, recommendation } | null
 *  - predictionError: string | null
 *  - showUploadWarning: boolean — true if user clicked predict with no image
 */
export default function PredictionResult({
  imagePreview,
  predictionResult,
  predictionError,
  showUploadWarning
}) {
  if (showUploadWarning) {
    return (
      <div className="nutri-warning" style={{ marginTop: "1rem" }}>
        Please upload a leaf image before running the analysis.
      </div>
    );
  }

  if (predictionError) {
    return (
      <div className="nutri-warning" style={{ marginTop: "1rem" }}>
        {predictionError}
      </div>
    );
  }

  if (!predictionResult) return null;

  return (
    <>
      <div className="leaf-frame">
        <img src={imagePreview} alt="Analyzed leaf" />
      </div>

      <br />

      <div className="result-grid">
        <DiagnosisCard
          label={predictionResult.prediction}
          confidence={predictionResult.confidence}
        />
        <RecommendationCard recommendation={predictionResult.recommendation} />
      </div>
    </>
  );
}
