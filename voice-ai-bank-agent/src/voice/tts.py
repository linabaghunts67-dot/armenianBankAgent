import pyttsx3


class TextToSpeech:
    """
    Improved TTS with:
    - voice selection
    - speed control
    - stability
    """

    def __init__(self):
        self.engine = pyttsx3.init()
        self._configure_voice()

    def _configure_voice(self):
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', int(rate * 0.9)) 

        voices = self.engine.getProperty('voices')

        selected_voice = None

        for voice in voices:
            name = voice.name.lower()

            if "female" in name or "zira" in name or "anna" in name:
                selected_voice = voice.id
                break

        if not selected_voice and voices:
            selected_voice = voices[0].id

        if selected_voice:
            self.engine.setProperty('voice', selected_voice)

    def speak(self, text: str):
        if not text:
            return

        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[TTS Error]: {e}")


tts_instance = TextToSpeech()


def speak(text: str):
    tts_instance.speak(text)
