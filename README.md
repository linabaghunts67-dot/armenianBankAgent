# 🎙️ Armenian Voice AI Bank Assistant — UPDATED

A real-time, voice-enabled AI agent that answers customer questions in Armenian about **credits, deposits, and branch locations** for three Armenian banks — strictly grounded in scraped data from their official websites.

Built with the **open-source LiveKit Agents framework** (not LiveKit Cloud).

---

## 🏗️ Architecture & Design Decisions

### System Architecture

```
User Microphone
      ↓
LiveKit Room (WebRTC, self-hosted open-source server)
      ↓
Deepgram Nova-2 STT  ←── Armenian language (hy)
      ↓
GPT-4o-mini (with injected bank context)
      ↓
OpenAI TTS (alloy voice)
      ↓
LiveKit Room → User Speaker
```

### Why LiveKit Open-Source?

The requirement specifies open-source LiveKit, not LiveKit Cloud. We use:
- `livekit-agents` SDK — the official Python framework for building voice agents
- A **self-hosted LiveKit server** (runs locally via Docker or binary)
- This gives full real-time WebRTC audio streaming with VAD (Voice Activity Detection)

### Why Deepgram for STT?

Deepgram Nova-2 is the best production-grade STT with Armenian (`hy`) language support available as a LiveKit plugin. It offers low latency (~300ms) and accurate transcription for Armenian speech.

### Why GPT-4o-mini?

- **Armenian language support**: natively understands and generates Armenian text
- **Speed**: ~1–2s response time, suitable for voice conversations
- **Cost**: significantly cheaper than GPT-4o, and more than sufficient for constrained Q&A over a small knowledge base
- **Guardrails**: temperature set to 0.1 to minimize hallucination; the system prompt strictly restricts answers to provided context only

### Why OpenAI TTS instead of pyttsx3?

`pyttsx3` uses the OS's built-in voice engine (espeak on Linux, SAPI on Windows). **No major OS ships an Armenian voice**, so pyttsx3 either fails silently or speaks English phonetics. OpenAI TTS (`tts-1`, `alloy` voice) natively supports Armenian text with natural pronunciation.

### Guardrails

The LLM is given a strict system prompt that:
1. Injects all scraped bank data as the **only allowed knowledge source**
2. Restricts answers to three topics: credits, deposits, branch locations
3. Forces an Armenian refusal message for any out-of-scope question:
   > "Ես չեմ կարող պատասխանել այդ հարցին։ Կարող եմ օգնել միայն վարկերի, ավանդների և մասնաճյուղերի վերաբերյալ հարցերում։"

### Data Sources

Bank data is scraped from the official websites of three Armenian banks:

| Bank | Website |
|------|---------|
| Ameriabank | https://www.ameriabank.am |
| Ardshinbank | https://www.ardshinbank.am |
| ACBA Bank | https://www.acba.am |

The scraper fetches credits, deposits, and branch location pages from each bank and saves them to `data/bank_data.json`. The system is designed to scale to any number of banks — just add entries to `scraper/scraper.py`.

---

## 📁 Project Structure

```
armenianBankAgent/
└── voice-ai-bank-agent/
    ├── data/
    │   └── bank_data.json          # Scraped bank data (auto-generated)
    ├── scraper/
    │   └── scraper.py              # Web scraper for bank websites
    ├── src/
    │   ├── __init__.py
    │   ├── main.py                 # Entry point (LiveKit or CLI mode)
    │   ├── ai.py                   # LLM logic + context injection + guardrails
    │   ├── livekit_agent.py        # Real LiveKit open-source agent
    │   └── voice/
    │       ├── __init__.py
    │       ├── stt.py              # STT (CLI mode fallback)
    │       └── tts.py              # TTS using OpenAI (Armenian-capable)
    ├── requirements.txt
    └── README.md
```

---

## ⚙️ Setup & Run Guide

### 1. Clone the repository

```bash
git clone https://github.com/linabaghunts67-dot/armenianBankAgent.git
cd armenianBankAgent/voice-ai-bank-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Linux note**: If PyAudio fails, install portaudio first: `sudo apt-get install portaudio19-dev`
> **Linux TTS note**: Install mpg123 for audio playback: `sudo apt-get install mpg123`

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in:
- `OPENAI_API_KEY` — from https://platform.openai.com
- `DEEPGRAM_API_KEY` — from https://console.deepgram.com (free tier works)
- `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` — from your local LiveKit server (see below)

### 5. Start a local LiveKit server

```bash
# Using Docker (recommended):
docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp \
  -e LIVEKIT_KEYS="devkey: secret" \
  livekit/livekit-server --dev
```

Or download the binary from https://github.com/livekit/livekit/releases

### 6. Scrape bank data (optional — pre-scraped data is included)

```bash
python scraper/scraper.py
```

### 7. Run the agent

**LiveKit mode** (full real-time voice):
```bash
python -m src.main --mode livekit
```

Then connect a client to your LiveKit room (e.g. using the LiveKit Meet example app or any WebRTC client).

**CLI mode** (local microphone testing, no LiveKit needed):
```bash
python -m src.main --mode cli
```

---

## 🧪 Example Interaction

```
🎤 Speak... (Speak in Armenian)
Դուք: Ի՞նչ ավանդներ ունի Ամերիաբանկը
AI: Ամերիաբանկում հնարավոր է բացել ժամկետային ավանդներ ՀՀ դրամով, ԱՄՆ դոլարով և եվրոյով։ ...

🎤 Speak...
Դուք: Ո՞րն է լավ ռեստորան Երևանում
AI: Ես չեմ կարող պատասխանել այդ հարցին։ Կարող եմ օգնել միայն վարկերի, ավանդների և մասնաճյուղերի վերաբերյալ հարցերում։
```

---

## 🛠️ Tech Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| Voice framework | LiveKit Agents (open-source) | Required; real-time WebRTC |
| STT | Deepgram Nova-2 | Best Armenian support, low latency |
| LLM | GPT-4o-mini | Armenian support, fast, cheap |
| TTS | OpenAI TTS (alloy) | Native Armenian, unlike pyttsx3 |
| Data | Scraped JSON (beautifulsoup4) | Grounded, no hallucination |
