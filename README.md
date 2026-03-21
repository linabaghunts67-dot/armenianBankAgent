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

This ensures **reliable, explainable, and safe AI behavior**, avoiding hallucinations and maintaining full control over outputs.

---

## ✨ Key Features

*  **Context-Constrained LLM**
  Answers are generated strictly from structured bank data

*  **Full Voice Pipeline**
  Speech-to-Text → AI → Text-to-Speech

*  **Armenian Language Support**

*  **Strict Guardrails**
  Out-of-scope queries are safely rejected

*  **Modular Architecture**
  Clean separation between AI, voice, and data components

---

## 🏗️ Architecture & Design Decisions

### System Architecture

```text
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

The project follows a **modular architecture**:

* `ai.py` → AI logic, prompt construction, guardrails
* `voice/stt.py` → Speech-to-text processing
* `voice/tts.py` → Text-to-speech output
* `livekit_agent.py` → Real-time voice system integration layer
* `bank_data.json` → Structured knowledge base

This design enables:

* scalability
* maintainability
* easy extension (e.g., adding new banks or upgrading to RAG)

---

### Context-Based AI (Core Design Choice)

Instead of relying on general model knowledge:

* All banking data is stored in a JSON file
* The data is injected directly into the prompt
* The model is instructed to answer **only using this context**

This ensures:

* no hallucinations
* full control over answers
* predictable system behavior

---

### Guardrails & Safety

To enforce safe and reliable responses:

* Allowed topics:

  * credits
  * deposits
  * branch locations
* Out-of-scope questions →
  **"Ես չեմ կարող պատասխանել այդ հարցին"**

The model is explicitly restricted from using external knowledge.

---

### Model Choice

**Model used:** `gpt-4o-mini`

Chosen because:

* fast and efficient (low latency for voice interaction)
* strong multilingual capabilities (supports Armenian)
* cost-effective for real-time use

---

### Voice Stack Design

* **SpeechRecognition** → lightweight speech-to-text
* **pyttsx3** → offline text-to-speech (reliable, no API dependency)
* **LiveKit (integration layer)** → included to support real-time voice system design and future streaming upgrades

---

### Scalability

The system is designed to scale easily:

* Add new banks → extend JSON
* Add new topics → update dataset + prompt
* Upgrade to RAG → replace JSON with vector database
* Real-time streaming → extend LiveKit integration

---

## 📁 Project Structure

```text
voice-ai-bank-agent/
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
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/linabaghunts67-dot/armenian_bank_AI.git
cd armenian_bank_AI
```

---

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_api_key_here
```

⚠️ Do not include quotes
⚠️ Do not upload `.env` to GitHub

---

## ▶️ Run the Application

```bash
python -m src.main
```

---

## 🧪 Example Interaction

```text
🎤 Speak...
Դու: Ի՞նչ վարկեր ունի Ամերիաբանկը
AI: Ամերիաբանկը տրամադրում է սպառողական և հիփոթեքային վարկեր...
```

---

## 🛠️ Tech Stack

* Python
* OpenAI GPT-4o-mini
* SpeechRecognition
* pyttsx3
* LiveKit (integration layer)
* python-dotenv

---

## 📈 Future Improvements

* Full LiveKit real-time streaming
* Vector database (RAG pipeline)
* Web interface (FastAPI / Streamlit)
* Expanded dataset with detailed bank information

---

## ⭐ Project Value

This project demonstrates:

* practical LLM system design
* controlled AI generation (no hallucinations)
* voice-based interaction pipeline
* readiness for real-world AI applications

---

<p align="center">
  ⭐ If you find this project useful, consider starring the repository ⭐
</p>
