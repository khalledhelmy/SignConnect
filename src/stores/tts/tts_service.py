import torch
from transformers import AutoProcessor, AutoModelForTextToSpectrogram, SpeechT5HifiGan
from datasets import load_dataset
import os
from helpers.config import settings  

class TTsService:
    def __init__(self):
        os.makedirs(settings.HF_CACHE_DIR_tts, exist_ok=True)

        self.processor = AutoProcessor.from_pretrained(
            settings.BASE_MODEL_tts,
            cache_dir=settings.HF_CACHE_DIR_tts,
            token=settings.HF_TOKEN_tts
        )

        self.model = AutoModelForTextToSpectrogram.from_pretrained(
            settings.BASE_MODEL_tts,
            cache_dir=settings.HF_CACHE_DIR_tts,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            token=settings.HF_TOKEN_tts
        )

        self.vocoder = SpeechT5HifiGan.from_pretrained(
            settings.VOCODER_MODEL_tts,
            token=settings.HF_TOKEN_tts
        )

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.model.eval()

        dataset = load_dataset(
            "Matthijs/cmu-arctic-xvectors",
            split="validation",
            cache_dir=settings.HF_CACHE_DIR_tts,
            token=settings.HF_TOKEN_tts
        )

        self.speaker_embedding = torch.tensor(
            dataset[settings.SPEAKER_INDEX]["xvector"]
        ).unsqueeze(0).to(self.device)

    def tts(self, text: str):
        inputs = self.processor(text=text, return_tensors="pt").to(self.device)

        with torch.no_grad():
            speech = self.model.generate_speech(
                inputs["input_ids"],
                self.speaker_embedding,
                vocoder=self.vocoder
            )

        return speech.cpu().numpy()  
