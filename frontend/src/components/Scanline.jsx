import React, { useEffect, useState } from "react";

/**
 * Reproduces the Streamlit `.scanline` div — a thin green line that
 * sweeps down the viewport once, 1.8s after the app loads.
 */
export default function Scanline() {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setVisible(false), 1800);
    return () => clearTimeout(timer);
  }, []);

  if (!visible) return null;

  return <div className="scanline" />;
}
