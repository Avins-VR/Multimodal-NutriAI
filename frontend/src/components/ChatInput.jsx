import React from "react";

/**
 * Props:
 *  - value: string
 *  - onChange: (value: string) => void
 *  - onSend: () => void
 *  - onClear: () => void
 *  - isLoading: boolean
 */
export default function ChatInput({ value, onChange, onSend, onClear, isLoading }) {
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !isLoading && value.trim()) {
      onSend();
    }
  };

  return (
    <div className="chat-input-wrap">
      <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
        <input
          type="text"
          className="chat-text-input"
          placeholder="Ask about crops, soil, pests…"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <button
          type="button"
          className="chat-send-button"
          onClick={onSend}
          disabled={isLoading || !value.trim()}
        >
          ➤
        </button>
      </div>

      <div style={{ textAlign: "center", marginTop: "0.6rem" }}>
        <button
          type="button"
          className="nutri-button"
          style={{ width: "auto", padding: "0.4rem 1rem" }}
          onClick={onClear}
        >
          Clear Chat
        </button>
      </div>
    </div>
  );
}
