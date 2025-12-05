import torch
from transformers import AutoProcessor, AutoModelForTextToSpectrogram, SpeechT5HifiGan
from datasets import load_dataset
import os
from helpers.config import settings  

class TTsService:
    def __init__(self):
        os.makedirs(settings.HF_CACHE_DIR_tts, exist_ok=True)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_dtype = torch.float16 if self.device == "cuda" else torch.float32

        self.processor = AutoProcessor.from_pretrained(
            settings.BASE_MODEL_tts,
            cache_dir=settings.HF_CACHE_DIR_tts,
            token=settings.HF_TOKEN_tts
        )

        self.model = AutoModelForTextToSpectrogram.from_pretrained(
            settings.BASE_MODEL_tts,
            cache_dir=settings.HF_CACHE_DIR_tts,
            torch_dtype=self.model_dtype,
            token=settings.HF_TOKEN_tts
        ).to(self.device)
        self.model.eval()


        self.vocoder = SpeechT5HifiGan.from_pretrained(
            settings.VOCODER_MODEL_tts,
            token=settings.HF_TOKEN_tts
        ).to(self.device).to(self.model_dtype)

        dataset = load_dataset(
            "Matthijs/cmu-arctic-xvectors",
            split="validation",
            cache_dir=settings.HF_CACHE_DIR_tts,
            token=settings.HF_TOKEN_tts
        )
        self.speaker_embedding = torch.tensor(
            dataset[settings.SPEAKER_INDEX]["xvector"]
        ).unsqueeze(0).to(self.device).to(self.model_dtype)

    def tts(self, text: str):
        inputs = self.processor(text=text, return_tensors="pt")
        inputs = {
            k: v.to(self.device).to(self.model_dtype)
            if v.dtype.is_floating_point else v.to(self.device)
            for k, v in inputs.items()
        }

        with torch.no_grad():
            speech = self.model.generate_speech(
                inputs["input_ids"],
                self.speaker_embedding,
                vocoder=self.vocoder
            )

        return speech.cpu().numpy()
