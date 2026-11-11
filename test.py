"""Standalone voice-assistant experiment from the historical prototype."""
from datetime import datetime
from random import choice

import pyttsx3
import speech_recognition as sr
from utils import opening_text


def speak(text):
    engine = pyttsx3.init("sapi5")  # Windows SAPI voice
    engine.say(text)
    engine.runAndWait()


def take_user_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-IN")
    except (sr.UnknownValueError, sr.RequestError) as exc:
        print(f"Speech recognition failed: {exc}")
        speak("Sorry, I could not understand. Could you please say that again?")
        return None

    if "exit" in query.lower() or "stop" in query.lower():
        hour = datetime.now().hour
        if hour >= 21 or hour < 6:
            speak("Good night sir, take care!")
        else:
            speak("Have a good day sir!")
        return query

    speak(choice(opening_text))
    return query


if __name__ == "__main__":
    take_user_input()
