from deep_translator import GoogleTranslator
from gtts import gTTS

class Spoker:
    def __init__(self,src_text:str):
        self.src_text = src_text
        self.trans_text = None
        self.audio = None
        self.filename = "gtts.mp3"

    def speak(self):
        translator = GoogleTranslator(source="en",target="es")
        self.trans_text = translator.translate(self.src_text)
        self.audio = gTTS(self.trans_text,lang="es-ES")

    def save_mp3(self):
        self.speak()
        self.audio.save(f"{self.filename}.mp3")

