import React from "react";

/**
 * Reproduces the full-width "⬡ Run Deficiency Analysis" button.
 *
 * Props:
 *  - onClick: () => void
 *  - isLoading: boolean
 */
export default function PredictionButton({ onClick, isLoading }) {
  return (
    <button
      type="button"
      className="predict-btn"
      onClick={onClick}
      disabled={isLoading}
    >
      {isLoading ? "⬡  Analyzing…" : "⬡  Run Deficiency Analysis"}
    </button>
  );
}
