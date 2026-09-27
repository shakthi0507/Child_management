from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.core.dependencies import require_role


router = APIRouter(prefix="/therapist", tags=["Therapist Help"])
VIDEO_PATH = Path(__file__).resolve().parents[2] / "videos" / "therapist_video.mp4"


@router.get("/help-video")
def get_therapist_help_video(
    therapist=Depends(require_role("THERAPIST")),
):
    if not VIDEO_PATH.is_file():
        raise HTTPException(status_code=404, detail="Therapist help video is unavailable")
    return FileResponse(VIDEO_PATH, media_type="video/mp4")
