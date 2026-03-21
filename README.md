# 🎙️ Voice AI Bank Assistant

### Context-Grounded Armenian Banking Assistant with Real-Time Voice Interaction

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-black?style=flat-square"/>
  <img src="https://img.shields.io/badge/Voice-AI-orange?style=flat-square"/>
</p>

---

## 🚀 Overview

This project implements a **voice-enabled AI banking assistant** that answers user queries in Armenian using a **strictly controlled knowledge base**.

The system simulates a real-world fintech AI agent by enforcing:

* context grounding
* response constraints
* modular architecture

This ensures **reliable and safe AI behavior**, avoiding hallucinations.

---

## ✨ Key Features

* Context-Constrained LLM
* Full Voice Pipeline (STT → AI → TTS)
* Armenian Language Support
* Guardrails (no hallucinations)
* Modular Architecture

---

## 🏗️ Architecture & Design Decisions

### System Architecture

```
User Speech
   ↓
Speech-to-Text (SpeechRecognition)
   ↓
AI Engine (OpenAI + Context Injection)
   ↓
Text Response
   ↓
Text-to-Speech (pyttsx3)
   ↓
Voice Output
```

---

### Design Overview

* `ai.py` → AI logic and guardrails
* `voice/stt.py` → Speech-to-text
* `voice/tts.py` → Text-to-speech
* `livekit_agent.py` → Real-time agent layer
* `data/bank_data.json` → Knowledge base

---

### Model Choice

* **gpt-4o-mini** → fast, cost-efficient, supports Armenian

---

### Guardrails

* Allowed topics:

  * credits
  * deposits
  * branch locations
* Out-of-scope →
  **"Ես չեմ կարող պատասխանել այդ հարցին"**

---

## 📁 Project Structure

```
armenianBankAgent/
│
└── voice-ai-bank-agent/
    │
    ├── data/
    │   └── bank_data.json
    │
    ├── src/
    │   ├── main.py
    │   ├── ai.py
    │   ├── livekit_agent.py
    │   └── voice/
    │       ├── stt.py
    │       └── tts.py
    │
    ├── requirements.txt
    ├── .env
    └── README.md
```

---

# ⚙️ Setup & Run Guide

## 1. Clone the repository

```bash
git clone https://github.com/linabaghunts67-dot/armenianBankAgent.git
cd armenianBankAgent/voice-ai-bank-agent
```

---

## 2. Go into the project folder

```bash
cd voice-ai-bank-agent
```

---

## 3. Create virtual environment (recommended)

```bash
python -m venv venv
```

### Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Create `.env` file

Create a file named `.env` inside `voice-ai-bank-agent/`:

```
OPENAI_API_KEY=your_api_key_here
```

⚠️ Do NOT upload `.env` to GitHub

---

## ▶️ Run the Application

```bash
python -m src.main
```

---

## 🧪 Example

```
🎤 Speak...
Դու: Ի՞նչ ավանդներ ունի Ամերիաբանկը
AI: Ամերիաբանկում հնարավոր է բացել ժամկետային ավանդներ...
```

---

## 🛠️ Tech Stack

* Python
* OpenAI GPT-4o-mini
* SpeechRecognition
* pyttsx3
* LiveKit (lightweight integration)
* python-dotenv

---

## 📈 Future Improvements

* Full LiveKit real-time streaming
* RAG (vector database)
* Web interface
* Expanded dataset
  
---

<p align="center">
  ⭐ If you find this project useful, consider starring the repo ⭐
</p>
