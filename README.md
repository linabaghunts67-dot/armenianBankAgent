<div align="center">

# 🎙️ Armenian Voice AI Bank Assistant

<p>A real-time voice AI agent that answers customer questions <strong>in Armenian</strong> about credits, deposits, and branch locations — strictly grounded in data scraped from official bank websites.</p>

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![LiveKit](https://img.shields.io/badge/LiveKit-Open--Source-orange?style=for-the-badge&logo=webrtc&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-black?style=for-the-badge&logo=openai&logoColor=white)
![Deepgram](https://img.shields.io/badge/Deepgram-Armenian_STT-green?style=for-the-badge&logo=microphone&logoColor=white)

</div>

---

## 📁 Project Structure
```
voice-ai-bank-agent/
├── data/
│   └── bank_data.json          # Scraped bank data
├── scraper/
│   └── scraper.py              # Scrapes 3 Armenian bank websites
├── src/
│   ├── voice/
│   │   ├── stt.py              # Speech-to-Text (Google, hy-AM)
│   │   └── tts.py              # Text-to-Speech (OpenAI TTS)
│   ├── ai.py                   # LLM engine + guardrails
│   ├── livekit_agent.py        # Real-time LiveKit agent
│   └── main.py                 # Entry point
├── requirements.txt
└── README.md
```

---

## 🏗️ Architecture

### Full Pipeline
```
User Microphone
      │
      ▼
LiveKit Room (WebRTC — self-hosted open-source server)
      │
      ▼
Silero VAD (filters silence)
      │
      ▼
Deepgram Nova-2 STT (language: hy — Armenian)
      │
      ▼
GPT-4o-mini ◄── bank_data.json injected as system context
(only credits / deposits / branch locations allowed)
      │
      ▼
OpenAI TTS (alloy voice — supports Armenian)
      │
      ▼
LiveKit Room → User Speaker
```

### CLI Mode (local testing, no LiveKit needed)
```
Microphone → SpeechRecognition (hy-AM) → GPT-4o-mini → OpenAI TTS → Speaker
```

---

## 🧠 Design Decisions

### Why LiveKit Open-Source?
The requirement specifies open-source LiveKit, not LiveKit Cloud. We use the `livekit-agents` Python SDK with a **self-hosted LiveKit server via Docker** — full WebRTC audio pipeline with no dependency on any commercial cloud.

### Why Deepgram Nova-2 for STT?
Deepgram is the only production-grade STT with Armenian (`hy`) support available as a native LiveKit plugin. Latency is ~300ms — fast enough for natural conversation. Whisper alternatives average ~1–2s which feels sluggish in voice chat.

### Why GPT-4o-mini?
- Natively understands and generates Armenian
- ~1–2s response time — suitable for real-time voice
- ~15× cheaper than GPT-4o, more than sufficient for constrained Q&A
- Temperature set to `0.1` to minimize hallucination

### Why OpenAI TTS instead of pyttsx3?
`pyttsx3` uses the OS built-in voice engine. **No OS ships an Armenian voice** — it would either crash or mispronounce everything. OpenAI TTS (`alloy` voice) natively handles Armenian script with natural pronunciation.

### Guardrails
The system prompt:
1. Injects all of `bank_data.json` as the **only permitted knowledge**
2. Restricts answers to: credits, deposits, branch locations
3. Returns a fixed Armenian refusal for anything else:
> *"Ես չեմ կարող պատասխանել այդ հարցին։ Կարող եմ օгнел миайն варкери, авандери ев маснаjyughneri веraberjal харцеrum։"*

### Data Sources

| Bank | Website |
|------|---------|
| Ameriabank | https://www.ameriabank.am |
| Ardshinbank | https://www.ardshinbank.am |
| ACBA Bank | https://www.acba.am |

Adding a new bank = adding 3 lines to `SCRAPE_TARGETS` in `scraper/scraper.py`.

---

## ⚙️ Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/linabaghunts67-dot/armenianBankAgent.git
cd armenianBankAgent/voice-ai-bank-agent
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
> **Linux:** `sudo apt-get install portaudio19-dev mpg123`

### 4. Set up environment variables
```bash
cp .env.example .env
```
Fill in `.env`:
```env
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

### 5. Start local LiveKit server
```bash
docker run --rm \
  -p 7880:7880 -p 7881:7881 -p 7882:7882/udp \
  -e LIVEKIT_KEYS="devkey: secret" \
  livekit/livekit-server --dev
```

### 6. (Optional) Re-scrape bank data
```bash
python scraper/scraper.py
```

### 7. Run the agent

**LiveKit mode** (full real-time voice):
```bash
python -m src.main --mode livekit
```

**CLI mode** (local mic, no LiveKit needed):
```bash
python -m src.main --mode cli
```

---

## 🧪 Example
```
🎤 Speak...
Դուք:  Ի՞նչ ավանդներ ունի Ամերիաբանկը
AI:    Ամերիաբանկում հնարավոր է բացել ժամկետային ավանդներ ՀՀ դրամով, ԱՄՆ դոլարով և եվրոյով։

🎤 Speak...
Դուք:  Ո՞ր ռեստորանն է լավ Երևանում
AI:    Ես չեմ կարող պատասխանել այդ հարցին։ Կարող եմ օгнел миайн варкери, авандери ев маснаjyughneri веraberjal харцеrum։
```

---

## 🛠️ Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Voice framework | LiveKit Agents (open-source) | Real-time WebRTC, self-hosted |
| VAD | Silero | Filters silence, reduces API costs |
| STT | Deepgram Nova-2 (`hy`) | Best Armenian STT, ~300ms latency |
| LLM | GPT-4o-mini | Armenian support, fast, cheap |
| TTS | OpenAI TTS (`alloy`) | Native Armenian — pyttsx3 has no Armenian voice |
| Scraping | requests + BeautifulSoup4 | Lightweight HTML parsing |
| Knowledge Base | JSON | Simple, inspectable, version-controlled |
