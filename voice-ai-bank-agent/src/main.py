from src.ai import load_data, ask_ai
from src.voice.stt import listen
from src.voice.tts import speak
from src.livekit_agent import LiveKitAgent


def run():
    data = load_data()

    agent = LiveKitAgent()
    agent.start()

    while True:
        user_input = listen()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            break

        response = ask_ai(user_input, data)
        print("AI:", response)

        speak(response)


if __name__ == "__main__":
    run()