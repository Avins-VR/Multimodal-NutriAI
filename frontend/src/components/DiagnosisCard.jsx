import React from "react";

const COLOR_MAP = {
  Healthy: { accent: "#2ea043", bg: "#0d2e17" },
  "Early Deficiency": { accent: "#d29922", bg: "#2b2008" },
  "Critical Deficiency": { accent: "#f85149", bg: "#2d0f0e" }
};

export default function DiagnosisCard({ label, confidence }) {
  const { accent, bg } = COLOR_MAP[label] || { accent: "#7dd9a8", bg: "#0b1a12" };

  return (
    <div
      className="result-card"
      style={{
        borderLeft: `3px solid ${accent}`,
        background: `linear-gradient(135deg, ${bg} 0%, rgba(255,255,255,0.02) 100%)`
      }}
    >
      <div className="result-label">Diagnosis</div>
      <div className="result-value" style={{ color: accent, fontSize: "1.55rem" }}>
        {label}
      </div>
      <span
        className="result-badge"
        style={{
          background: "rgba(255,255,255,0.05)",
          color: accent,
          border: `1px solid ${accent}40`
        }}
      >
        {confidence.toFixed(1)}% confidence
      </span>
      <div className="confidence-bar" style={{ marginTop: "10px" }}>
        <div
          className="confidence-fill"
          style={{
            width: `${confidence.toFixed(1)}%`,
            background: `linear-gradient(90deg, ${bg}, ${accent})`
          }}
        />
      </div>
    </div>
  );
}
