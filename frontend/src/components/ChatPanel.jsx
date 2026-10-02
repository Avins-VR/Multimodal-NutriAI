import React, { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage.jsx";
import ChatInput from "./ChatInput.jsx";

export default function ChatPanel({
  chatMessages,
  chatInput,
  onChatInputChange,
  onSend,
  onClear,
  isChatLoading,
  chatError
}) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [chatMessages]);

  return (
    <div className="col-chat">
      <div className="chat-panel-header">
        <div className="section-label">◈ Field Assistant Chat</div>
      </div>

      <div className="chat-container" ref={scrollRef}>
        {chatMessages.length === 0 ? (
          <div className="chat-empty">
            Ask me anything about
            <br />
            crops, soil, or plant health…
          </div>
        ) : (
          chatMessages.map((msg, idx) => (
            <ChatMessage key={idx} role={msg.role} content={msg.content} />
          ))
        )}
      </div>

      {chatError && (
        <div className="nutri-warning" style={{ margin: "0.6rem 1.2rem 0" }}>
          {chatError}
        </div>
      )}

      <ChatInput
        value={chatInput}
        onChange={onChatInputChange}
        onSend={onSend}
        onClear={onClear}
        isLoading={isChatLoading}
      />
    </div>
  );
}
