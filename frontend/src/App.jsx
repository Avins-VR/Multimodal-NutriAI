import React, { useState } from "react";
import Scanline from "./components/Scanline.jsx";
import Sidebar from "./components/Sidebar.jsx";
import MainContent from "./components/MainContent.jsx";
import ChatPanel from "./components/ChatPanel.jsx";
import usePrediction from "./hooks/usePrediction.js";
import { sendChatMessage } from "./services/api.js";

const DEFAULT_SOIL_DATA = {
  N: 50,
  P: 50,
  K: 50,
  ph: 6.5,
  soil_moisture: 20,
  temperature: 25,
  humidity: 50,
  rainfall: 80,
  sunlight_exposure: 8
};

export default function App() {
  // ── Soil parameters ──
  const [soilData, setSoilData] = useState(DEFAULT_SOIL_DATA);

  // ── Image upload ──
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [showUploadWarning, setShowUploadWarning] = useState(false);

  // ── Sidebar (mobile) ──
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // ── Prediction ──
  const { predictionResult, isPredicting, predictionError, predict, reset } =
    usePrediction();

  // ── Chat ──
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [chatError, setChatError] = useState(null);

  const handleSoilChange = (key, value) => {
    setSoilData((prev) => ({ ...prev, [key]: value }));
  };

  const handleFileSelect = (file) => {
    setUploadedImage(file);
    setImagePreview(URL.createObjectURL(file));
    setShowUploadWarning(false);
    reset();
  };

  const handleClearImage = () => {
    setUploadedImage(null);
    setImagePreview(null);
    reset();
  };

  const handlePredict = () => {
    if (!uploadedImage) {
      setShowUploadWarning(true);
      return;
    }
    setShowUploadWarning(false);
    predict(uploadedImage, soilData);
  };

  const handleSendChat = async () => {
    const trimmed = chatInput.trim();
    if (!trimmed || isChatLoading) return;

    const nextMessages = [...chatMessages, { role: "user", content: trimmed }];
    setChatMessages(nextMessages);
    setChatInput("");
    setIsChatLoading(true);
    setChatError(null);

    try {
      const reply = await sendChatMessage(nextMessages);
      setChatMessages((prev) => [...prev, { role: "assistant", content: reply }]);
    } catch (err) {
      setChatError(err.message || "Chatbot error, please try again.");
    } finally {
      setIsChatLoading(false);
    }
  };

  const handleClearChat = () => {
    setChatMessages([]);
    setChatError(null);
  };

  return (
    <div className="app-shell">
      <Scanline />

      <Sidebar
        soilData={soilData}
        onSoilChange={handleSoilChange}
        isSidebarOpen={isSidebarOpen}
        onOpenSidebar={() => setIsSidebarOpen(true)}
        onCloseSidebar={() => setIsSidebarOpen(false)}
      />

      <div className="main-columns">
        <MainContent
          imagePreview={imagePreview}
          onFileSelect={handleFileSelect}
          onClearImage={handleClearImage}
          onPredict={handlePredict}
          isPredicting={isPredicting}
          predictionResult={predictionResult}
          predictionError={predictionError}
          showUploadWarning={showUploadWarning}
        />

        <ChatPanel
          chatMessages={chatMessages}
          chatInput={chatInput}
          onChatInputChange={setChatInput}
          onSend={handleSendChat}
          onClear={handleClearChat}
          isChatLoading={isChatLoading}
          chatError={chatError}
        />
      </div>
    </div>
  );
}
