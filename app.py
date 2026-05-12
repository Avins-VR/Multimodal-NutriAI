import time
import streamlit as st
import torch
import os
import gdown
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import numpy as np
import cv2
import pandas as pd
import joblib
import requests

# ================================
# PAGE SETTINGS
# ================================
st.set_page_config(
    page_title="Multimodal NutriAI",
    page_icon="🌿",
    layout="wide"
)

MODEL_PATH = "image_model.pth"

def download_model():
    if not os.path.exists(MODEL_PATH):
        file_id = "1QQuBf5gwGVR36Bn3HanBU5H5gGbaYznA"
        url = f"https://drive.google.com/uc?id={file_id}"

        gdown.download(
            url,
            MODEL_PATH,
            quiet=False
        )
# ================================
# CUSTOM CSS — REDESIGNED UI
# ================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Reset & Base ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* Hide sidebar collapse/expand arrow button */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    button[data-testid="baseButton-header"] { display: none !important; }

    * { box-sizing: border-box; }

    /* Reduce default Streamlit top padding */
    .block-container {
        padding-top: 2rem !important;
        padding-right: 1.5rem !important;
    }

    .stApp {
        background-color: #080c0a;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% 0%, rgba(34, 90, 50, 0.18) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(16, 60, 35, 0.12) 0%, transparent 55%);
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #0b100d;
        border-right: 1px solid rgba(74, 150, 100, 0.15);
        width: 360px !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 0 !important;
    }

    /* ── Sidebar brand strip ── */
    .sidebar-brand {
        padding: 1.4rem 1.5rem 1rem;
        border-bottom: 1px solid rgba(74, 150, 100, 0.15);
        background: linear-gradient(135deg, rgba(34,90,50,0.25) 0%, rgba(11,16,13,0) 60%);
        margin-bottom: 0;
    }

    .sidebar-brand-icon {
        font-size: 1.8rem;
        line-height: 1;
    }

    .sidebar-brand-title {
        font-family: 'DM Serif Display', serif;
        color: #7dd9a8;
        font-size: 1.15rem;
        letter-spacing: 0.01em;
        margin-top: 4px;
        line-height: 1.2;
    }

    .sidebar-brand-sub {
        color: rgba(180, 220, 195, 0.45);
        font-size: 0.7rem;
        font-weight: 300;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-top: 2px;
    }

    /* ── Chat section label ── */
    .section-label {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: rgba(125, 217, 168, 0.55);
        padding: 1rem 1.5rem 0.5rem;
    }

    /* ── Chat container ── */
    .chat-container {
        height: 360px;
        overflow-y: auto;
        padding: 0.8rem 1rem;
        background: transparent;
        margin: 0 0.8rem;
        border: 1px solid rgba(74, 150, 100, 0.12);
        border-radius: 12px;
        background: rgba(255,255,255,0.015);
        scrollbar-width: thin;
        scrollbar-color: rgba(74,150,100,0.3) transparent;
    }

    .chat-container::-webkit-scrollbar { width: 4px; }
    .chat-container::-webkit-scrollbar-track { background: transparent; }
    .chat-container::-webkit-scrollbar-thumb { background: rgba(74,150,100,0.3); border-radius: 2px; }

    .chat-empty {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: rgba(125, 217, 168, 0.3);
        font-size: 0.78rem;
        font-style: italic;
        text-align: center;
    }

    /* ── Chat bubbles ── */
    .bubble-row-user { display: flex; justify-content: flex-end; margin: 7px 0; }
    .bubble-row-bot  { display: flex; justify-content: flex-start; margin: 7px 0; align-items: flex-start; gap: 6px; }

    .bot-avatar {
        width: 22px; height: 22px;
        background: linear-gradient(135deg, #1e5c35, #2a8a52);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.65rem;
        flex-shrink: 0;
        margin-top: 2px;
    }

    .user-bubble {
        background: linear-gradient(135deg, #1a5c35 0%, #155229 100%);
        color: #c8f0da;
        padding: 7px 11px;
        border-radius: 14px 14px 3px 14px;
        font-size: 0.82rem;
        line-height: 1.45;
        max-width: 82%;
        border: 1px solid rgba(74,170,100,0.2);
    }

    .assistant-bubble {
        background: rgba(255,255,255,0.04);
        color: #b8d4c2;
        padding: 7px 11px;
        border-radius: 3px 14px 14px 14px;
        font-size: 0.82rem;
        border: 1px solid rgba(74,150,100,0.14);
        line-height: 1.5;
        max-width: 85%;
    }

    /* ── Chat input row ── */
    .chat-input-wrap {
        padding: 0.6rem 0.8rem 0.3rem;
    }

    .stTextInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(74,150,100,0.25) !important;
        color: #d4ead9 !important;
        border-radius: 8px !important;
        font-size: 0.83rem !important;
        font-family: 'DM Sans', sans-serif !important;
        padding: 8px 12px !important;
        transition: border-color 0.2s !important;
    }

    .stTextInput input:focus {
        border-color: rgba(125,217,168,0.55) !important;
        box-shadow: 0 0 0 3px rgba(74,150,100,0.1) !important;
        outline: none !important;
    }

    .stTextInput input::placeholder { color: rgba(125,180,148,0.35) !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #1e6b3d 0%, #165c32 100%) !important;
        color: #a8f0c8 !important;
        border: 1px solid rgba(74,170,100,0.3) !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s ease !important;
        padding: 0.45rem 0.9rem !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #247d47 0%, #1b6e3a 100%) !important;
        border-color: rgba(125,217,168,0.45) !important;
        box-shadow: 0 4px 16px rgba(34,130,70,0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Divider ── */
    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(74,150,100,0.12);
        margin: 0.8rem 0;
    }

    /* ── Soil data section ── */
    .soil-section {
        padding: 0 1rem 1rem;
    }

    /* Slider override — green accent */
    [data-testid="stSlider"] > div > div > div > div {
        background: linear-gradient(90deg, #1e6b3d, #2a9455) !important;
    }

    [data-testid="stSlider"] > div > div > div > div > div {
        background: #7dd9a8 !important;
        border: 2px solid #0b100d !important;
        box-shadow: 0 0 8px rgba(125,217,168,0.4) !important;
        width: 14px !important;
        height: 14px !important;
    }

    [data-testid="stSlider"] p,
    [data-testid="stSlider"] label {
        color: rgba(180,220,195,0.7) !important;
        font-size: 0.76rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 400 !important;
    }

    /* Slider value pill */
    [data-testid="stSlider"] [data-baseweb="slider"] span {
        color: #7dd9a8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem !important;
        background: rgba(34,100,60,0.25) !important;
        border: 1px solid rgba(74,150,100,0.2) !important;
        border-radius: 4px !important;
        padding: 1px 5px !important;
    }

    /* Slider track background */
    [data-baseweb="slider"] > div:first-child {
        background: rgba(74,150,100,0.15) !important;
    }

    /* ── MAIN AREA ── */
    .main-hero {
        padding: 2.5rem 0 1.5rem;
        text-align: center;
        position: relative;
    }

    .hero-eyebrow {
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: rgba(125,217,168,0.55);
        margin-bottom: 0.6rem;
        font-family: 'DM Sans', sans-serif;
    }

    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.8rem;
        color: #e8f5ed;
        line-height: 1.1;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .hero-title em {
        font-style: italic;
        color: #7dd9a8;
    }

    .hero-sub {
        color: rgba(180,220,195,0.45);
        font-size: 0.88rem;
        font-weight: 300;
        letter-spacing: 0.02em;
    }

    /* ── Upload zone ── */
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(255,255,255,0.02) !important;
        border: 1.5px dashed rgba(74,150,100,0.3) !important;
        border-radius: 14px !important;
        transition: border-color 0.2s, background 0.2s !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: rgba(125,217,168,0.55) !important;
        background: rgba(34,100,60,0.06) !important;
    }

    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] span {
        color: rgba(125,180,148,0.55) !important;
        font-size: 0.82rem !important;
    }

    /* ── Predict button full-width ── */
    .predict-btn .stButton > button {
        background: linear-gradient(135deg, #1a6b3c 0%, #0f4d28 100%) !important;
        color: #9ef5c4 !important;
        font-size: 0.9rem !important;
        padding: 0.65rem 1.2rem !important;
        border-radius: 10px !important;
        letter-spacing: 0.04em !important;
        border: 1px solid rgba(100,200,130,0.3) !important;
        box-shadow: 0 2px 20px rgba(20,110,55,0.2) !important;
    }

    .predict-btn .stButton > button:hover {
        box-shadow: 0 6px 28px rgba(20,110,55,0.4) !important;
    }

    /* ── Result cards ── */
    .result-grid {
        display: grid;
        gap: 10px;
        margin-top: 1rem;
    }

    .result-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(74,150,100,0.15);
        border-radius: 12px;
        padding: 14px 16px;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s;
    }

    .result-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.02) 0%, transparent 60%);
        pointer-events: none;
    }

    .result-label {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: rgba(125,180,148,0.5);
        margin-bottom: 6px;
        font-family: 'DM Sans', sans-serif;
    }

    .result-value {
        font-family: 'DM Serif Display', serif;
        color: #e8f5ed;
        font-size: 1.25rem;
        line-height: 1.2;
    }

    .result-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        font-family: 'DM Sans', sans-serif;
        margin-top: 4px;
    }

    .confidence-bar {
        height: 4px;
        border-radius: 2px;
        background: rgba(74,150,100,0.15);
        margin-top: 8px;
        overflow: hidden;
    }

    .confidence-fill {
        height: 100%;
        border-radius: 2px;
        background: linear-gradient(90deg, #1e6b3d, #7dd9a8);
        transition: width 0.8s ease;
    }

    .rec-text {
        font-family: 'DM Sans', sans-serif;
        color: #a0c8b0;
        font-size: 0.85rem;
        line-height: 1.6;
        font-weight: 300;
    }

    /* ── Probability mini-bars ── */
    .prob-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 5px 0;
    }

    .prob-name {
        font-size: 0.72rem;
        color: rgba(160,200,170,0.65);
        width: 130px;
        flex-shrink: 0;
        font-family: 'JetBrains Mono', monospace;
    }

    .prob-track {
        flex: 1;
        height: 5px;
        background: rgba(74,150,100,0.12);
        border-radius: 3px;
        overflow: hidden;
    }

    .prob-fill {
        height: 100%;
        border-radius: 3px;
    }

    .prob-pct {
        font-size: 0.68rem;
        font-family: 'JetBrains Mono', monospace;
        color: rgba(125,217,168,0.65);
        width: 38px;
        text-align: right;
        flex-shrink: 0;
    }

    /* ── Image frame ── */
    .leaf-frame {
        border: 1px solid rgba(74,150,100,0.2);
        border-radius: 14px;
        overflow: hidden;
        background: rgba(255,255,255,0.02);
        padding: 6px;
    }

    /* ── Warning box ── */
    .stWarning {
        background: rgba(180,140,20,0.08) !important;
        border: 1px solid rgba(200,160,40,0.25) !important;
        border-radius: 10px !important;
        color: #d4b060 !important;
    }

    /* ── Scan line animation on load ── */
    @keyframes scanline {
        0%   { transform: translateY(-100%); opacity: 0.6; }
        100% { transform: translateY(100vh); opacity: 0; }
    }

    .scanline {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(125,217,168,0.4), transparent);
        animation: scanline 1.8s ease-out forwards;
        pointer-events: none;
        z-index: 9999;
    }
</style>

<div class="scanline"></div>
""", unsafe_allow_html=True)

# ================================
# CONFIG
# ================================
class_names = ["Healthy", "Early Deficiency", "Critical Deficiency"]

features = [
    "N", "P", "K",
    "ph",
    "soil_moisture",
    "temperature",
    "humidity",
    "rainfall",
    "sunlight_exposure"
]

device = torch.device("cpu")

# ================================
# LOAD MODELS (cached)
# ================================
@st.cache_resource
def load_models():
    class DSEE(nn.Module):
        def __init__(self, in_channels):
            super().__init__()

            self.h = nn.Conv2d(in_channels, in_channels, (1,3), padding=(0,1))
            self.v = nn.Conv2d(in_channels, in_channels, (3,1), padding=(1,0))
            self.d1 = nn.Conv2d(in_channels, in_channels, 3, padding=1)
            self.d2 = nn.Conv2d(in_channels, in_channels, 3, padding=1)
            self.r = nn.Conv2d(in_channels, in_channels, 3, padding=1)

            self.fusion = nn.Conv2d(in_channels*5, in_channels, 1)
            self.bn = nn.BatchNorm2d(in_channels)
            self.relu = nn.ReLU()

        def forward(self, x):
            h = self.h(x)
            v = self.v(x)
            d1 = self.d1(x)
            d2 = self.d2(x)
            r = self.r(x)

            out = torch.cat([h, v, d1, d2, r], dim=1)
            out = self.fusion(out)
            out = self.bn(out)
            out = self.relu(out)

            return out + x


    class ImageModel(nn.Module):
        def __init__(self):
            super().__init__()

            self.backbone = models.efficientnet_b3(weights=None)
            self.features = self.backbone.features

            self.dsee = DSEE(1536)
            self.pool = nn.AdaptiveAvgPool2d(1)

            self.classifier = nn.Sequential(
                nn.Linear(1536, 256),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Dropout(0.4),
                nn.Linear(128, 3)
            )

        def forward(self, x):
            f = self.features(x)
            e = self.dsee(f)

            fused = f + 0.5 * e

            pooled = self.pool(fused)
            pooled = pooled.view(pooled.size(0), -1)

            return self.classifier(pooled)

    download_model()

    img_model = ImageModel()
    img_model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    img_model.eval()

    rf = joblib.load("rf_metadata_model.pkl")
    sc = joblib.load("rf_scaler.pkl")
    df = pd.read_csv("train_data.csv")

    return img_model, rf, sc, df


image_model, rf_model, scaler, data_df = load_models()
rf_classes = rf_model.classes_

# ================================
# MISTRAL CLIENT
# ================================
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
mistral_client = MistralClient(api_key=MISTRAL_API_KEY)

# ================================
# TRANSFORM
# ================================
transform = transforms.Compose([
    transforms.Resize((300, 300)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ================================
# PREDICTION FUNCTIONS
# ================================
def image_prediction(image):
    img_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = image_model(img_tensor)
        probs = torch.softmax(outputs, dim=1).numpy()[0]
    return probs


def metadata_prediction(metadata_dict):
    df = pd.DataFrame([metadata_dict])
    scaled = scaler.transform(df[features])
    probs = rf_model.predict_proba(scaled)[0]
    ordered = np.zeros(len(class_names))
    for i, cls in enumerate(rf_classes):
        idx = class_names.index(cls)
        ordered[idx] = probs[i]
    return ordered


def fusion(img_prob, meta_prob):
    return 0.7 * img_prob + 0.3 * meta_prob


def get_recommendation(metadata_dict, predicted_class):
    class_data = data_df[data_df["Label"] == predicted_class]
    X = scaler.transform(class_data[features])
    y = class_data["Recommendation"].values
    input_scaled = scaler.transform(pd.DataFrame([metadata_dict])[features])
    dist = np.linalg.norm(X - input_scaled, axis=1)
    idx = np.random.choice(np.argsort(dist)[:5])
    return y[idx]


# ================================
# CHATBOT FUNCTIONS
# ================================
def check_agriculture(question: str) -> bool:
    try:
        time.sleep(0.5)

        classify_prompt = f"""You are a strict topic classifier. Reply with EXACTLY one word: YES or NO.

Is the following question related to agriculture, farming, crops, soil, fertilizers, irrigation, plant diseases, livestock, or pests?

Question: {question}

Reply only YES or NO."""

        response = mistral_client.chat(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": classify_prompt}]
        )

        # ✅ FIX: correct parsing
        result = response.choices[0].message.content.strip().upper()

        return result.startswith("YES")

    except Exception as e:
        st.error(f"Chatbot error: {e}")
        return False


def get_agriculture_response(chat_history: list) -> str:
    try:
        time.sleep(0.5)

        system_instruction = {
            "role": "user",
            "content": """
You are a strict agriculture assistant.

RULES:
- Answer ONLY agriculture-related questions.
- Agriculture includes: crops, soil, fertilizers, irrigation, pests, plant diseases, farming techniques.
- If the question is NOT related to agriculture, reply EXACTLY with:
"I'm scoped to agriculture topics only — try asking about crops, soil health, fertilizers, irrigation, or pests."

- Keep answers concise.
- Use bullet points or steps when needed.
"""
        }

        response = mistral_client.chat(
            model="mistral-small-latest",
            messages=[system_instruction] + chat_history
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {e}"

# ================================
# SESSION STATE
# ================================
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "chat_input_key" not in st.session_state:
    st.session_state.chat_input_key = 0

# ================================
# SIDEBAR — BRAND + SOIL SLIDERS ONLY
# ================================
with st.sidebar:

    # ── Brand strip ──
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🌿</div>
        <div class="sidebar-brand-title">Multimodal NutriAI</div>
        <div class="sidebar-brand-sub">Nutrient Intelligence System</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Soil Data Section ──
    st.markdown('<div class="section-label">◈ Soil & Environment Parameters</div>', unsafe_allow_html=True)

    st.markdown('<div class="soil-section">', unsafe_allow_html=True)
    metadata = {}
    metadata["N"]                 = st.slider("Nitrogen (N) · mg/kg",       0,    135,  50)
    metadata["P"]                 = st.slider("Phosphorus (P) · mg/kg",      0,    135,  50)
    metadata["K"]                 = st.slider("Potassium (K) · mg/kg",       0,    135,  50)
    metadata["ph"]                = st.slider("pH Level",                    3.5,  9.9,  6.5)
    metadata["soil_moisture"]     = st.slider("Soil Moisture · %",           0.0,  45.0, 20.0)
    metadata["temperature"]       = st.slider("Temperature · °C",            0.0,  40.0, 25.0)
    metadata["humidity"]          = st.slider("Humidity · %",                10.0, 100.0,50.0)
    metadata["rainfall"]          = st.slider("Rainfall · mm",               0.0,  170.0,80.0)
    metadata["sunlight_exposure"] = st.slider("Sunlight Exposure · hrs/day", 1.0,  20.0, 8.0)
    st.markdown('</div>', unsafe_allow_html=True)


# ================================
# MAIN AREA — TWO COLUMN LAYOUT
# col_main : upload + predict + results  (left/center)
# col_chat : chatbot panel               (right)
# ================================

col_main, col_chat = st.columns([3, 2])

# ── RIGHT COLUMN — CHATBOT ──────────────────────────────────────
with col_chat:
    st.markdown("""
    <div style="padding-top:0.8rem; padding-left:1.2rem;">
        <div class="section-label" style="padding-left:0;">◈ Field Assistant Chat</div>
    </div>
    """, unsafe_allow_html=True)

    # Render chat history
    chat_html = '<div class="chat-container" id="chat-box" style="height:470px; margin:0; margin-left:1.2rem;">'
    if not st.session_state.chat_messages:
        chat_html += '<div class="chat-empty">Ask me anything about<br>crops, soil, or plant health…</div>'
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            chat_html += f'<div class="bubble-row-user"><div class="user-bubble">{msg["content"]}</div></div>'
        else:
            chat_html += f'<div class="bubble-row-bot"><div class="bot-avatar">🌱</div><div class="assistant-bubble">{msg["content"]}</div></div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Chat input row
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    col_spacer, col_inp, col_btn = st.columns([0.2, 5, 1])
    with col_inp:
        user_input = st.text_input(
            label="chat",
            label_visibility="collapsed",
            placeholder="Ask about crops, soil, pests…",
            key=f"chat_input_{st.session_state.chat_input_key}"
        )
    with col_btn:
        send_clicked = st.button("➤", key="send_btn")

    if send_clicked and user_input.strip():
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        with st.spinner(""):
            reply = get_agriculture_response(st.session_state.chat_messages)

        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

        st.session_state.chat_input_key += 1
        st.rerun()
    col_clr1, col_clr2, col_clr3 = st.columns([1.5, 2, 0.5])
    with col_clr2:
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()


# ── LEFT/CENTER COLUMN — HERO + UPLOAD + RESULTS ───────────────
with col_main:

    # ── Hero header ──
    st.markdown("""
    <div class="main-hero" style="padding-top:0.4rem;">
        <div class="hero-eyebrow">Vision + Soil Fusion Model</div>
        <div class="hero-title">Leaf <em>Deficiency</em><br>Detection</div>
        <div class="hero-sub">Upload a leaf image · set soil parameters · get instant diagnosis</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload + Predict ──
    uploaded_file = st.file_uploader(
        "Drop leaf image here — JPG, JPEG or PNG",
        type=["jpg", "jpeg", "png"],
        label_visibility="visible"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="predict-btn">', unsafe_allow_html=True)
    predict_clicked = st.button("⬡  Run Deficiency Analysis", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ================================
    # PREDICTION OUTPUT
    # ================================
    if uploaded_file is not None and predict_clicked:
        image = Image.open(uploaded_file).convert("RGB")

        img_prob   = image_prediction(image)
        meta_prob  = metadata_prediction(metadata)
        final_prob = fusion(img_prob, meta_prob)

        predicted   = np.argmax(final_prob)
        label       = class_names[predicted]
        confidence  = np.max(final_prob) * 100

        recommendation = get_recommendation(metadata, label)

        image_np   = np.array(image)
        result_img = cv2.resize(image_np, (400, 400))

        # ── Leaf image with frame ──
        st.markdown('<div class="leaf-frame">', unsafe_allow_html=True)
        st.image(result_img, use_container_width=False, width=400)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Color map ──
        color_map = {
            "Healthy":             ("#2ea043", "#0d2e17"),
            "Early Deficiency":    ("#d29922", "#2b2008"),
            "Critical Deficiency": ("#f85149", "#2d0f0e"),
        }
        accent, bg_tint = color_map.get(label, ("#7dd9a8", "#0b1a12"))

        # ── Status card ──
        st.markdown(f"""
        <div class="result-card" style="border-left: 3px solid {accent}; background: linear-gradient(135deg, {bg_tint} 0%, rgba(255,255,255,0.02) 100%);">
            <div class="result-label">Diagnosis</div>
            <div class="result-value" style="color:{accent}; font-size:1.55rem;">{label}</div>
            <span class="result-badge" style="background:rgba(255,255,255,0.05); color:{accent}; border:1px solid {accent}40;">
                {confidence:.1f}% confidence
            </span>
            <div class="confidence-bar" style="margin-top:10px;">
                <div class="confidence-fill" style="width:{confidence:.1f}%; background:linear-gradient(90deg,{bg_tint},{accent});"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Recommendation card ──
        st.markdown(f"""
        <div class="result-card" style="border-left:3px solid rgba(180,140,80,0.5);">
            <div class="result-label">💡 Field Recommendation</div>
            <div class="rec-text">{recommendation}</div>
        </div>
        """, unsafe_allow_html=True)

    elif predict_clicked and uploaded_file is None:
        st.warning("Please upload a leaf image before running the analysis.")
