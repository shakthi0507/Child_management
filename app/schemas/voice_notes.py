from datetime import datetime

from pydantic import BaseModel





class VoiceNoteResponse(BaseModel):


    id: int


    child_id: int


    parent_id: int


    goal_id: int | None


    domain: str | None

    confidence: int | None


    audio_path: str


    language: str | None


    transcribed_text: str | None


    ai_match_status: str | None


    therapist_review: str | None

    ai_summary: str | None

    ai_suggestion: str | None

    review_status: str | None

    therapist_comment: str | None


    created_at: datetime



    class Config:

        from_attributes = True