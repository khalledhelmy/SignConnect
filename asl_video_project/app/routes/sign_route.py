from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.sign_model import create_video_for_letter

router = APIRouter(prefix="/api")

@router.get("/video")
def get_video(letter: str):
    try:
        # create_video_for_letter returns a file-like object (BytesIO) positioned at start
        video_io = create_video_for_letter(letter)
        return StreamingResponse(video_io, media_type="video/mp4")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))