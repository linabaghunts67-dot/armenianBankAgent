import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="hy-AM")
        print("You:", text)
        return text
    except:
        return ""