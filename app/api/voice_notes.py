from pydantic import BaseModel

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException
)

from sqlalchemy.orm import Session



import uuid
import logging
import mimetypes
import os
from pathlib import Path
from fastapi.responses import FileResponse


from app.database.deps import get_db

from app.models.voice_notes import VoiceNote

from app.models.user import User

from app.models.goal import Goal

from app.services.voice_matching_service import (
    match_voice_note
)

from app.schemas.voice_notes import (
    VoiceNoteResponse
)

from app.core.dependencies import (
    get_current_user,
    ensure_child_access,
    require_role
)

from app.services.transcription import (
    transcribe_audio
)

from app.services.voice_ai_service import generate_voice_insights



router = APIRouter(
    prefix="/voice-notes",
    tags=["Voice Notes"]
)



UPLOAD_DIR = "uploads/audio"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIO_ROOT = PROJECT_ROOT / UPLOAD_DIR
if os.getenv("VOICE_STORAGE_DIR"):
    AUDIO_ROOT = Path(os.environ["VOICE_STORAGE_DIR"]).expanduser().resolve()
MAX_AUDIO_BYTES = 10 * 1024 * 1024
ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",
    "audio/mp4",
    "audio/wav",
    "audio/x-wav",
    "audio/webm",
}


AUDIO_ROOT.mkdir(parents=True, exist_ok=True)


def resolve_audio_path(audio_path: str) -> Path:
    root = AUDIO_ROOT.resolve()
    stored_path = Path(audio_path)
    candidate = stored_path.resolve() if stored_path.is_absolute() else (root / stored_path.name).resolve()
    if not candidate.is_relative_to(root):
        raise HTTPException(404, "Voice recording not found")
    return candidate





# ===================================
# Parent uploads voice note
# ===================================

@router.post(
    "/upload",
    response_model=VoiceNoteResponse
)
async def upload_voice(

    child_id: int = Form(...),

    file: UploadFile = File(...),

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)

):


    parent = db.query(User).filter(User.id == current_user["id"]).first()

    child = ensure_child_access(child_id, current_user, db)
    if current_user["role"] != "PARENT" or parent is None or parent.id != child.parent_id:
        raise HTTPException(403, "Only the child's parent can upload voice notes")

    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(400, "Unsupported audio type")


    if not parent:

        raise HTTPException(
            404,
            "Parent not found"
        )



    filename = (

        f"{uuid.uuid4()}_{Path(file.filename or 'voice-note').name}"

    )


    file_path = AUDIO_ROOT / filename



    size = 0
    try:
        with open(file_path, "wb") as buffer:
            while chunk := file.file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_AUDIO_BYTES:
                    raise HTTPException(413, "Audio file is too large")
                buffer.write(chunk)
    except HTTPException:
        file_path.unlink(missing_ok=True)
        raise
    except Exception as exc:
        file_path.unlink(missing_ok=True)
        raise HTTPException(500, "Audio processing failed") from exc

    result = None
    try:
        result = transcribe_audio(str(file_path))
    except Exception as exc:
        logging.getLogger(__name__).warning(
            "Voice transcription unavailable (%s)", type(exc).__name__
        )

    transcript = (result or {}).get("text")
    transcript = transcript.strip() if isinstance(transcript, str) else ""
    if not transcript:
        transcript = None

    goals = (

        db.query(
            Goal
        )

        .filter(
            Goal.child_id == child_id
        )

        .all()

    )



    if transcript:
        try:
            match = match_voice_note(transcript, goals)
            insights = generate_voice_insights(
                transcript,
                match["domain"],
                match.get("title"),
            )
        except Exception as exc:
            logging.getLogger(__name__).warning(
                "Voice-note enrichment unavailable (%s)", type(exc).__name__
            )
            match = {"goal_id": None, "domain": None, "confidence": None}
            insights = {"ai_summary": None, "ai_suggestion": None}
    else:
        match = {"goal_id": None, "domain": None, "confidence": None}
        insights = {"ai_summary": None, "ai_suggestion": None}


    # AI matching will come here
    #
    # Example:
    #
    # Speech text
    #      |
    #      v
    # Speech Goal
    #
    # matched_goal_id = AI result


    voice_note = VoiceNote(

        child_id=child_id,

        parent_id=parent.id,

        goal_id=match["goal_id"],

        domain=match["domain"],

        confidence=match["confidence"],

        audio_path=filename,

        language=(result or {}).get("language") if transcript else None,

        transcribed_text=transcript,

        ai_summary=insights["ai_summary"],

        ai_suggestion=insights["ai_suggestion"],

        review_status="PENDING"

    )



    db.add(
        voice_note
    )

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        file_path.unlink(missing_ok=True)
        raise HTTPException(500, "Voice note could not be saved") from exc

    db.refresh(
        voice_note
    )


    return voice_note







# ===================================
# Parent/Therapist view child voices
# ===================================


@router.get(
    "/child/{child_id}",
    response_model=list[VoiceNoteResponse]
)
def get_child_voice_notes(

    child_id:int,

    db:Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):
    ensure_child_access(child_id, current_user, db)
    return (
        db.query(VoiceNote)
        .filter(VoiceNote.child_id == child_id)
        .all()
    )


@router.get("/{voice_note_id}/audio")
def get_voice_note_audio(
    voice_note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    voice_note = db.query(VoiceNote).filter(VoiceNote.id == voice_note_id).first()
    if not voice_note:
        raise HTTPException(404, "Voice note not found")
    ensure_child_access(voice_note.child_id, current_user, db)
    if current_user["role"] == "PARENT" and voice_note.parent_id != current_user["id"]:
        raise HTTPException(403, "Access denied")

    file_path = resolve_audio_path(voice_note.audio_path)
    if not file_path.is_file():
        raise HTTPException(404, "Voice recording not found")
    media_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    return FileResponse(
        file_path,
        media_type=media_type,
        headers={
            "Cache-Control": "private, no-store",
            "X-Content-Type-Options": "nosniff",
        },
    )


@router.delete("/{voice_note_id}")
def delete_voice_note(
    voice_note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    voice_note = db.query(VoiceNote).filter(VoiceNote.id == voice_note_id).first()
    if not voice_note:
        raise HTTPException(404, "Voice note not found")

    ensure_child_access(voice_note.child_id, current_user, db)
    if current_user["role"] == "PARENT" and voice_note.parent_id != current_user["id"]:
        raise HTTPException(403, "Access denied")

    resolve_audio_path(voice_note.audio_path).unlink(missing_ok=True)
    db.delete(voice_note)
    db.commit()
    return {"message": "Voice note deleted successfully"}


class VoiceReviewUpdate(BaseModel):
    therapist_comment: str
    review_status: str = "REVIEWED"


@router.put("/{voice_note_id}/review", response_model=VoiceNoteResponse)
def review_voice_note(
    voice_note_id: int,
    data: VoiceReviewUpdate,
    db: Session = Depends(get_db),
    therapist=Depends(require_role("THERAPIST")),
):
    voice_note = db.query(VoiceNote).filter(VoiceNote.id == voice_note_id).first()
    if not voice_note:
        raise HTTPException(404, "Voice note not found")
    ensure_child_access(voice_note.child_id, therapist, db, allow_admin=False)
    if data.review_status not in {"PENDING", "REVIEWED", "FLAGGED"}:
        raise HTTPException(400, "Invalid review status")
    voice_note.therapist_comment = data.therapist_comment
    voice_note.therapist_review = data.therapist_comment
    voice_note.review_status = data.review_status
    db.commit()
    db.refresh(voice_note)
    return voice_note
