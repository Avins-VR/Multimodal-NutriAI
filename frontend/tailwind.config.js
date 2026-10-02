/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        nutri: {
          background: "#080c0a",
          sidebar: "#0b100d",
          primary: "#7dd9a8",
          darkGreen: "#1e6b3d",
          darkGreen2: "#165c32",
          darkGreen3: "#1a6b3c",
          darkGreen4: "#0f4d28",
          text: "#e8f5ed",
          textMuted: "#b8d4c2",
          textFaint: "#a0c8b0",
          healthy: "#2ea043",
          healthyBg: "#0d2e17",
          early: "#d29922",
          earlyBg: "#2b2008",
          critical: "#f85149",
          criticalBg: "#2d0f0e"
        }
      },
      fontFamily: {
        "serif-display": ["DM Serif Display", "serif"],
        sans: ["DM Sans", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"]
      }
    }
  },
  plugins: []
};
