import React from "react";
import Hero from "./Hero.jsx";
import ImageUploader from "./ImageUploader.jsx";
import PredictionButton from "./PredictionButton.jsx";
import PredictionResult from "./PredictionResult.jsx";

export default function MainContent({
  imagePreview,
  onFileSelect,
  onClearImage,
  onPredict,
  isPredicting,
  predictionResult,
  predictionError,
  showUploadWarning
}) {
  return (
    <div className="col-main">
      <Hero />

      <ImageUploader
        imagePreview={imagePreview}
        onFileSelect={onFileSelect}
        onClear={onClearImage}
      />

      <br />

      <PredictionButton onClick={onPredict} isLoading={isPredicting} />

      <PredictionResult
        imagePreview={imagePreview}
        predictionResult={predictionResult}
        predictionError={predictionError}
        showUploadWarning={showUploadWarning}
      />
    </div>
  );
}
