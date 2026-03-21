"""
livekit_agent.py — Real LiveKit open-source agent using livekit-agents SDK.

Architecture:
  User microphone → LiveKit room (STT via Deepgram) → GPT-4o-mini (context-grounded)
  → TTS via OpenAI TTS → LiveKit room → User speaker

Why these models:
  - Deepgram Nova-2: best Armenian STT available via LiveKit plugin, low latency
  - GPT-4o-mini: supports Armenian, fast, cheap, sufficient for constrained Q&A
  - OpenAI TTS (alloy): supports Armenian output reliably, unlike pyttsx3 which has no Armenian voice
"""

import json
import os
import asyncio
from dotenv import load_dotenv

from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, openai, silero

load_dotenv()

BANK_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bank_data.json")


def load_bank_context() -> str:
    """Load scraped bank data and format as context string."""
    with open(BANK_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    context_blocks = []
    for entry in data:
        context_blocks.append(
            f"Բանկ: {entry['bank']}\nՈլորտ: {entry['topic']}\nՏեղեկություն: {entry['content']}"
        )
    return "\n\n".join(context_blocks)


def build_system_prompt() -> str:
    context = load_bank_context()
    return f"""Դու հայկական բանկային AI օգնական ես։

ԽԻՍՏ ԿԱՆՈՆՆԵՐ:
- Պատասխանիր ԲԱՑԱՌԱՊԵՍ ստորև տրված բանկային տվյալների հիման վրա։
- Թույլատրված թեմաներ: վարկեր (credits), ավանդներ (deposits), մասնաճյուղերի հասցեներ (branch locations)։
- Եթե հարցը վերաբերում է այլ թեմայի → պատասխանիր. "Ես չեմ կարող պատասխանել այդ հարցին։ Կարող եմ օգնել միայն վարկերի, ավանդների և մասնաճյուղերի վերաբերյալ հարցերում։"
- ՄԻ օգտագործիր արտաքին գիտելիքներ կամ ենթադրություններ։
- Պատասխանիր հայերեն։
- Կարճ, հստակ, ճշգրիտ պատասխաններ տուր։

ԲԱՆԿԱՅԻՆ ՏՎՅԱԼՆԵՐ (միայն սրանք օգտագործիր):
{context}
"""


async def entrypoint(ctx: JobContext):
    """Main LiveKit agent entrypoint — called when a user connects to the room."""

    system_prompt = build_system_prompt()

    initial_chat_ctx = llm.ChatContext().append(
        role="system",
        text=system_prompt,
    )

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),                          
        stt=deepgram.STT(language="hy"),                
        llm=openai.LLM(model="gpt-4o-mini"),            
        tts=openai.TTS(voice="alloy"),                
        chat_ctx=initial_chat_ctx,
    )

    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say(
        "Բարև ձեզ։ Ես հայկական բանկային AI օգնականն եմ։ Կարող եմ օգնել վարկերի, ավանդների և մասնաճյուղերի վերաբերյալ հարցերում։",
        allow_interruptions=True,
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint)
    )
