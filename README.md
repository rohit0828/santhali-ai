# 🌍 Santhali AI Assistant 

[![Live Demo](https://img.shields.io/badge/Live_Demo-Play_Now-brightgreen?style=for-the-badge)](https://santhali-ai.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-Fast_Inference-f37626?style=for-the-badge)](https://groq.com/)
[![LLaMA 3.1](https://img.shields.io/badge/Meta-LLaMA_3.1-043b72?style=for-the-badge&logo=meta&logoColor=white)](https://ai.meta.com/llama/)

A mobile-optimized, real-time conversational AI assistant designed exclusively for native Santhali speakers. This project bridges the digital divide for low-resource languages by allowing users to interact with state-of-the-art LLMs entirely in the native **Ol Chiki** script.

### 🚀 Live Application
**Try it out here:** [santhali-ai.streamlit.app](https://santhali-ai.streamlit.app)

---

## 📖 The Problem & Our Solution
Large Language Models (LLMs) are predominantly trained on high-resource languages (English, Spanish, etc.). Native Santhali speakers are often forced to cognitively translate their thoughts into English or Hindi before using modern AI tools. 

Directly fine-tuning an LLM on Santhali is computationally expensive and suffers from severe tokenization fragmentation. **Santhali AI** solves this by engineering a lightweight, ultra-fast **Translation Pipeline Architecture** that acts as an intermediary bridge between the user and Meta's LLaMA 3.1 model.

## ✨ Key Features
* 🔡 **Native Ol Chiki Support:** Full input and output support for the Santhali language.
* ⚡ **Ultra-Low Latency:** Powered by Groq's Language Processing Units (LPUs) for near-instantaneous AI inference.
* 🧠 **Conversational Memory:** Uses UUID-based session state to remember the chat history, allowing for fluid, natural follow-up questions.
* 📱 **Mobile-First UI:** A clean, messaging-app style interface built with Streamlit, optimized for mobile web browsers.
* 🔍 **English Verification:** An expandable UI layer that allows bilingual users to check the AI's internal English reasoning.

---

## ⚙️ How It Works (The Pipeline)
1. **Input:** The user types a query in Santhali (Ol Chiki).
2. **Bridge Translation (In):** The Santhali text is intercepted and translated into English using the Google Translate API.
3. **Inference:** The English prompt, along with the user's UUID session history, is routed to **LLaMA 3.1 (8B)** via the **Groq API**.
4. **Bridge Translation (Out):** The AI's English response is translated back into Santhali.
5. **Output:** The final Santhali response is rendered on the UI.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Python)
* **LLM Engine:** Meta LLaMA 3.1-8b 
* **Inference API:** Groq
* **Translation Bridge:** Google Translate API (`googletrans` / `deep-translator`)

---

## 💻 Run It Locally

Want to test or modify the code on your own machine? Follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/rohit0828/santhali-ai.git](https://github.com/rohit0828/santhali-ai.git)
   cd santhali-ai
