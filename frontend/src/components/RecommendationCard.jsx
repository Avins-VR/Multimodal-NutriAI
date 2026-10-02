import React from "react";

/**
 * Reproduces the Streamlit "💡 Field Recommendation" card.
 *
 * Props:
 *  - recommendation: string
 */
export default function RecommendationCard({ recommendation }) {
  return (
    <div
      className="result-card"
      style={{ borderLeft: "3px solid rgba(180,140,80,0.5)" }}
    >
      <div className="result-label">💡 Field Recommendation</div>
      <div className="rec-text">{recommendation}</div>
    </div>
  );
}
