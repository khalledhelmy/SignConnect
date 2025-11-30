from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from controller import TTSController
from models import TTSOutput
import io
import soundfile as sf

tts_router = APIRouter()
tts_controller = TTSController()

@tts_router.post("/Audio")
async def synthesize_text(text: str):
    audio_array, sr = tts_controller.synthesize(text)
    wav_io = io.BytesIO()
    sf.write(wav_io, audio_array, sr, format="WAV")
    wav_io.seek(0)
    return StreamingResponse(wav_io, media_type="audio/wav", headers={"X-Sampling-Rate": str(sr)})

