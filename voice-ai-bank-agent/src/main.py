"""
main.py — Entry point for the Armenian Voice AI Banking Assistant.

Two modes:
  1. LiveKit mode (default): Full real-time voice pipeline via LiveKit open-source server.
     Run: python -m src.main --mode livekit
  2. CLI mode (fallback for local testing without LiveKit):
     Run: python -m src.main --mode cli
"""

import argparse
import subprocess
import sys


def run_livekit_mode():
    print("🚀 Starting LiveKit Voice Agent...")
    print("   Make sure LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET are set in .env")
    print("   Waiting for users to join the LiveKit room...\n")
    subprocess.run([sys.executable, "-m", "src.livekit_agent"], check=True)


def run_cli_mode():
    from src.ai import load_data, ask_ai
    from src.voice.stt import listen
    from src.voice.tts import speak

    print("🎙️ Armenian Bank Assistant — CLI Mode")
    print("   Topics: credits (վարկեր), deposits (ավանդներ), branches (մասնաճյուղեր)")
    print("   Say 'exit' to quit.\n")

    data = load_data()

    while True:
        user_input = listen()

        if not user_input:
            continue

        if user_input.strip().lower() in {"exit", "quit", "դուրս"}:
            print("Ցտեսություն!")
            break

        response = ask_ai(user_input, data)
        print(f"AI: {response}\n")
        speak(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Armenian Bank Voice AI Agent")
    parser.add_argument(
        "--mode",
        choices=["livekit", "cli"],
        default="livekit",
        help="livekit = full real-time agent (default), cli = local mic test",
    )
    args = parser.parse_args()

    if args.mode == "livekit":
        run_livekit_mode()
    else:
        run_cli_mode()
