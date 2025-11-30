from pydantic import BaseModel

class TTSOutput(BaseModel):
    audio_base64: str
    sampling_rate: int

