import speech_recognition as sr


class SpeechToText:
    """
    Robust Speech-to-Text handler with:
    - noise adjustment
    - timeout handling
    - error handling
    - Armenian support
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Speak...")

            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=5,       
                    phrase_time_limit=8 
                )

            except sr.WaitTimeoutError:
                print("[STT] No speech detected.")
                return ""

        try:
            text = self.recognizer.recognize_google(
                audio,
                language="hy-AM"
            )

            print("Դու:", text)
            return text

        except sr.UnknownValueError:
            print("[STT] Could not understand audio.")
            return ""

        except sr.RequestError as e:
            print(f"[STT] API error: {e}")
            return ""


stt_instance = SpeechToText()


def listen():
    return stt_instance.listen()
