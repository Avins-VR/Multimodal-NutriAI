import React from "react";
import SoilSlider from "./SoilSlider.jsx";

export default function SoilParameters({ soilData, onChange }) {
  return (
    <>
      <div className="section-label">◈ Soil &amp; Environment Parameters</div>
      <div className="soil-section">
        <SoilSlider
          label="Nitrogen (N) · mg/kg"
          value={soilData.N}
          min={0}
          max={135}
          step={1}
          onChange={(v) => onChange("N", v)}
        />
        <SoilSlider
          label="Phosphorus (P) · mg/kg"
          value={soilData.P}
          min={0}
          max={135}
          step={1}
          onChange={(v) => onChange("P", v)}
        />
        <SoilSlider
          label="Potassium (K) · mg/kg"
          value={soilData.K}
          min={0}
          max={135}
          step={1}
          onChange={(v) => onChange("K", v)}
        />
        <SoilSlider
          label="pH Level"
          value={soilData.ph}
          min={3.5}
          max={9.9}
          step={0.1}
          decimals={1}
          onChange={(v) => onChange("ph", v)}
        />
        <SoilSlider
          label="Soil Moisture · %"
          value={soilData.soil_moisture}
          min={0}
          max={45}
          step={0.1}
          decimals={1}
          onChange={(v) => onChange("soil_moisture", v)}
        />
        <SoilSlider
          label="Temperature · °C"
          value={soilData.temperature}
          min={0}
          max={40}
          step={0.1}
          decimals={1}
          onChange={(v) => onChange("temperature", v)}
        />
        <SoilSlider
          label="Humidity · %"
          value={soilData.humidity}
          min={10}
          max={100}
          step={0.1}
          decimals={1}
          onChange={(v) => onChange("humidity", v)}
        />
        <SoilSlider
          label="Rainfall · mm"
          value={soilData.rainfall}
          min={0}
          max={170}
          step={0.1}
          decimals={1}
          onChange={(v) => onChange("rainfall", v)}
        />
        <SoilSlider
          label="Sunlight Exposure · hrs/day"
          value={soilData.sunlight_exposure}
          min={1}
          max={20}
          step={0.1}
          decimals={1}
          onChange={(v) => onChange("sunlight_exposure", v)}
        />
      </div>
    </>
  );
}
