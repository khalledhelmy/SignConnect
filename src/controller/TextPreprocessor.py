import re

class TextPreprocessor:
    @staticmethod
    def preprocess(text: str) -> str:
        text = re.sub(r"[^a-zA-Z0-9,.!?'\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        text = text.lower()
        return text.strip()
