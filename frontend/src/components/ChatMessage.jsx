import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * Props:
 *  - role: "user" | "assistant"
 *  - content: string
 */
export default function ChatMessage({ role, content }) {
  if (role === "user") {
    return (
      <div className="bubble-row-user">
        <div className="user-bubble">{content}</div>
      </div>
    );
  }

  return (
    <div className="bubble-row-bot">
      <div className="bot-avatar">🌱</div>

      <div className="assistant-bubble">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}