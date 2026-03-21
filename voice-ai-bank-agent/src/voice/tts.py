"""
tts.py — Text-to-Speech using OpenAI TTS API.

Why OpenAI TTS instead of pyttsx3:
  pyttsx3 relies on the OS's built-in voice engine (espeak / SAPI).
  No major OS ships an Armenian voice, so pyttsx3 would either fail silently
  or speak English phonetics. OpenAI TTS (model tts-1, voice "alloy") supports
  Armenian text natively with natural pronunciation.
"""

import os
import tempfile
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def speak(text: str) -> None:
    """Convert Armenian text to speech and play it."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",   
        input=text,
    )

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name
        response.stream_to_file(tmp_path)

    try:
        if os.name == "nt":  # Windows
            os.startfile(tmp_path)
        elif os.uname().sysname == "Darwin":  # macOS
            subprocess.run(["afplay", tmp_path], check=True)
        else:  # Linux
            subprocess.run(["mpg123", tmp_path], check=True)
    finally:
        os.unlink(tmp_path)
