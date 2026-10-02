import React from "react";
import SoilParameters from "./SoilParameters.jsx";

export default function Sidebar({
  soilData,
  onSoilChange,
  isSidebarOpen,
  onCloseSidebar,
  onOpenSidebar
}) {
  return (
    <>
      {/* Mobile "open sidebar" button — mirrors Streamlit's collapsedControl */}
      <button
        type="button"
        className="sidebar-toggle-btn"
        aria-label="Open sidebar"
        onClick={onOpenSidebar}
      >
        ☰
      </button>

      {/* Overlay behind the slide-in sidebar on mobile */}
      <div
        className={`sidebar-overlay ${isSidebarOpen ? "open" : ""}`}
        onClick={onCloseSidebar}
      />

      <aside className={`sidebar-panel ${isSidebarOpen ? "open" : ""}`}>
        <div className="sidebar-brand" style={{ position: "relative" }}>
          <button
            type="button"
            className="sidebar-close-btn"
            aria-label="Close sidebar"
            style={{ position: "absolute", top: 8, right: 8 }}
            onClick={onCloseSidebar}
          >
            ✕
          </button>
          <div className="sidebar-brand-main">
            <img
              src="../public/Multimodal Nutri AI.png"
              alt="NutriAI"
              className="sidebar-brand-image"
            />

            <div className="sidebar-brand-title">
              Multimodal NutriAI
            </div>
          </div>
          <div className="sidebar-brand-sub">Nutrient Intelligence System</div>
        </div>

        <SoilParameters soilData={soilData} onChange={onSoilChange} />
      </aside>
    </>
  );
}
