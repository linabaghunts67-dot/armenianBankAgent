"""
stt.py — Speech-to-Text using Google Speech Recognition with Armenian locale (hy-AM).
This is the CLI fallback mode. The LiveKit agent uses Deepgram for real-time STT.
"""

import speech_recognition as sr


def listen() -> str:
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.0

    with sr.Microphone() as source:
        print("Խոսեք... (Speak in Armenian)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("⏱ Timeout — no speech detected.")
            return ""

    try:
        text = recognizer.recognize_google(audio, language="hy-AM")
        print(f"Դուք: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"STT service error: {e}")
        return ""
