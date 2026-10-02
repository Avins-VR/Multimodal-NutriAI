import React from "react";

export default function Hero() {
  return (
    <div className="main-hero" style={{ paddingTop: 0 }}>
      <div className="hero-eyebrow">Vision + Soil Fusion Model</div>
      <div className="hero-title">
        Leaf <em>Deficiency</em>
        <br />
        Detection
      </div>
      <div className="hero-sub">
        Upload a leaf image · set soil parameters · get instant diagnosis
      </div>
    </div>
  );
}
