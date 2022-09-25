import os
from deep_translator import GoogleTranslator
from gtts import gTTS


class Spoker:
    def __init__(self, text: str):
        self.text = text
        self.audio = None
        self.filename = "gtts.wav"
        self.speech_rate = 1.20

    def save_audio(self):
        self.audio = gTTS(self.text, lang="es-ES")
        self.audio.save(f"{self.filename}_TEMP.mp3")
        os.system(
            f"ffmpeg -i {self.filename}_TEMP.mp3 -filter:a atempo={self.speech_rate} {self.filename}.wav -y")
        os.remove(f"{self.filename}_TEMP.mp3")
