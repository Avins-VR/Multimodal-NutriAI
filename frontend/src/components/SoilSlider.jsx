import React from "react";

/**
 * Custom-styled range input reproducing the Streamlit slider:
 * dark track, green active track, light green thumb, mono green value pill.
 *
 * Props:
 *  - label: string, e.g. "Nitrogen (N) · mg/kg"
 *  - value: number
 *  - min, max, step: number
 *  - onChange: (value: number) => void
 *  - decimals: how many decimal places to display in the value pill
 */
export default function SoilSlider({
  label,
  value,
  min,
  max,
  step = 1,
  onChange,
  decimals = 0
}) {
  const percent = ((value - min) / (max - min)) * 100;

  const displayValue =
    decimals > 0 ? Number(value).toFixed(decimals) : Math.round(value);

  return (
    <div className="mb-4">
      <div className="soil-slider-label">
        <span>{label}</span>
        <span className="soil-slider-value">{displayValue}</span>
      </div>
      <input
        type="range"
        className="soil-slider-input"
        min={min}
        max={max}
        step={step}
        value={value}
        style={{ "--slider-fill": `${percent}%` }}
        onChange={(e) => onChange(parseFloat(e.target.value))}
      />
    </div>
  );
}
