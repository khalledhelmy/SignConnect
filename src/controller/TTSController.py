from stores.tts import TTsService
from .TextPreprocessor import TextPreprocessor

class TTSController:
    def __init__(self):
        self.tts_service = TTsService()

    def synthesize(self, text: str):
        clean_text = TextPreprocessor.preprocess(text)
        audio_array = self.tts_service.tts(clean_text)
        return audio_array, 16000
    

