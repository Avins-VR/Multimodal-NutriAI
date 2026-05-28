# 🌿 Multimodal NutriAI  
### Multimodal Crop Nutrient Deficiency Detection System (with DSEE Architecture)

🔗 Live Demo: https://multimodal-nutriai.streamlit.app

---

## 🚨 Problem Statement

Farmers often struggle to identify crop nutrient deficiencies at the correct stage, leading to:

- ❌ Incorrect diagnosis based only on visual observation  
- ❌ Overuse or misuse of fertilizers  
- ❌ Reduced crop yield and increased costs  
- ❌ Lack of awareness of soil and environmental factors  

Most existing AI-based solutions rely **only on leaf images**, which results in:

- ⚠️ Incomplete understanding of plant health  
- ⚠️ Poor differentiation between early and critical deficiency stages  
- ⚠️ Ignoring key factors like soil nutrients and weather conditions  

👉 **Result:** Single-input models produce inaccurate or unreliable predictions.

---

## 💡 Proposed Solution

**Multimodal NutriAI** introduces a **Multimodal AI System** that combines:

1️⃣ **Leaf Image Analysis (CNN + DSEE)**  
2️⃣ **Soil & Environmental Data Analysis (ML Model)**  

👉 These two modalities are fused to generate **accurate, context-aware crop health predictions**.

---

## 🧠 Key Innovation: DSEE Architecture

### 🔹 Deficiency Shape Evolution Encoder (DSEE)

DSEE is a novel enhancement to traditional CNN architectures.

### 👉 What DSEE Does:

- Captures **shape transformation of deficiency patterns**
- Tracks **progressive evolution of leaf damage**
- Encodes:
  - Edges  
  - Spots  
  - Spread patterns  
- Learns **structural progression**, not just color features  

### 👉 Why It Matters:

| Traditional CNN | DSEE |
|---------------|------|
| Detects appearance | Understands evolution |
| Focuses on color/texture | Focuses on shape + progression |
| Struggles with early vs critical | Improves stage classification |

---

## 📸 1️⃣ Leaf Image Analysis (CNN + DSEE)

The system uses a **CNN enhanced with DSEE** to extract advanced visual features.

### 🔍 Detects:

- Yellowing → Nitrogen deficiency  
- Brown spots / edge burns  
- Texture irregularities  
- Disease-like stress patterns  
- Shape progression of damage (via DSEE)

👉 **Output:** High-level visual feature vector  

---

## 🌍 2️⃣ Soil & Environmental Metadata Analysis

A Machine Learning model processes environmental factors.

### 📥 Inputs:

- Nitrogen (N), Phosphorus (P), Potassium (K)  
- Soil pH  
- Soil moisture  
- Temperature  
- Rainfall  
- Sunlight exposure  

👉 **Output:** Environmental feature vector  

---

## 🔗 Multimodal Fusion Model

Both feature vectors are combined using a fusion layer:

```

Image Features (CNN + DSEE)
+
Metadata Features (ML Model)
↓
Fusion Layer
↓
Final Prediction Model
```


---

## 🎯 Final Classification

The system classifies crop health into:

- ✅ Healthy  
- 🟡 Early Deficiency  
- 🔴 Critical Deficiency  

---

## 📊 System Outputs

- Crop Health Status  
- Confidence Score  
- Fertilizer Recommendation  

### 🧪 Example:

```
Prediction: Early Deficiency
Confidence: 91%
Recommendation: Apply Nitrogen fertilizer
```
---

## 🤖 LLM-Based Chatbot

Multimodal NutriAI integrates an **LLM-powered chatbot** for better farmer interaction.

### ✨ Features:

- Natural language interaction  
- Context-aware responses  
- Smart recommendations  
- Easy-to-use interface  

### 💬 Example:

**Farmer:**  
"Why is my crop unhealthy?"

**Chatbot:**  
"Your soil nitrogen is low and moisture levels are insufficient. Apply nitrogen fertilizer and improve irrigation."

👉 Makes the system:

- User-friendly  
- Interactive  
- Scalable  

---

## ⚙️ System Workflow

1️⃣ Farmer uploads leaf image  
2️⃣ Inputs soil & environmental data  

3️⃣ CNN + DSEE processes image  
4️⃣ ML model processes metadata  

5️⃣ Fusion model combines both  

6️⃣ System outputs:
- Deficiency level  
- Confidence score  
- Fertilizer recommendation  

7️⃣ *(Future)* Improvement tracking system  

---

## 🔄 Future Work

### 🔹 Self-Learning Feedback System

- Track crop improvement over time  
- Compare before/after conditions  
- Learn from real-world outcomes  

👉 Enables:

- Continuous model improvement  
- Personalized recommendations  

---

## 🚀 What Makes Multimodal NutriAI Unique?

| Feature | Traditional Systems | Multimodal NutriAI |
|--------|-------------------|-------------------|
| Input Type | Only Image | Image + Metadata |
| Accuracy | Moderate | High |
| Deficiency Detection | Surface-level | Deep (with DSEE) |
| Evolution Understanding | ❌ | ✅ |
| Chatbot | Basic NLP | LLM-based |
| Learning Capability | ❌ | Future-ready |

---

## 🧩 Final Summary

**Multimodal NutriAI** is an intelligent agricultural system that combines:

- 📸 **Computer Vision (CNN + DSEE)**  
- 🌍 **Environmental Intelligence (ML Model)**  
- 🤖 **LLM-Based Interaction**  

👉 To deliver:

- Accurate predictions  
- Explainable insights  
- Farmer-friendly recommendations  

---

## 📌 Tech Stack (Optional)

- **Frontend:** React / Angular  
- **Backend:** Node.js / Flask  
- **ML Models:** CNN + DSEE, Scikit-learn  
- **Database:** PostgreSQL  
- **APIs:** OpenAI / Azure OpenAI  
- **Deployment:** Cloud / Edge-ready


## 👨‍💻 Author

**Avins V R**  
AI & Data Science Student  
AI & ML Developer

GitHub: https://github.com/Avins-VR
