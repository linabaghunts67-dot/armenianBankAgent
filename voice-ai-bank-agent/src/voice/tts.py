"""
tts.py — Text-to-Speech using OpenAI TTS API.

Why OpenAI TTS instead of pyttsx3:
  pyttsx3 has no Armenian voice on any OS — it would fail or speak gibberish.
  OpenAI TTS (alloy voice) natively supports Armenian.
"""

import os
import sys
import tempfile
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def speak(text: str) -> None:
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
        if sys.platform == "win32":       # Windows
            os.startfile(tmp_path)
        elif sys.platform == "darwin":    # macOS
            subprocess.run(["afplay", tmp_path], check=True)
        else:                             # Linux
            subprocess.run(["mpg123", tmp_path], check=True)
    finally:
        os.unlink(tmp_path)
