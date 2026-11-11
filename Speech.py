"""Original speech-input experiment, with minimal maintenance fixes."""
from pathlib import Path
import os

import speech_recognition as sr
from gtts import gTTS

AUDIO_FILE = Path(__file__).resolve().parent / "example.mp3"


def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    try:
        # Perform a single recognition request per recorded utterance.
        query = recognizer.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        return False
    except sr.RequestError as exc:
        print(f"Speech recognition request failed: {exc}")
        return False

    responses = {
        "你好": ("誠宜開張聖聽，以光先帝遺德，恢弘志士之氣，不宜妄自菲薄，引喻失義，以塞忠諫之路也", "zh"),
        "手機": ("no I am not", "en"),
    }
    response = responses.get(query)
    if response is None:
        print(f"No response mapped for: {query}")
        return False

    text, language = response
    gTTS(text=text, lang=language, slow=False).save(str(AUDIO_FILE))
    if os.name == "nt":
        os.startfile(str(AUDIO_FILE))  # Windows-specific historical setup
    else:
        print(f"Generated audio: {AUDIO_FILE}")
    return True


if __name__ == "__main__":
    while not speech_to_text():
        pass
