from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime
from app.models.child import Child

from app.models.goal import Goal

from app.database.base import Base



class VoiceNote(Base):

    __tablename__ = "voice_notes"

    child_id: int

    confidence: int | None

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    child_id = Column(
        Integer,
        ForeignKey(
            "children.id"
        ),
        nullable=False
    )

    confidence = Column(
        Integer
    )


    parent_id = Column(
        Integer,
        ForeignKey(
            "users.id"
        ),
        nullable=False
    )


    goal_id = Column(
        Integer,
        ForeignKey(
            "goals.id"
        ),
        nullable=True
    )


    domain = Column(
        String,
        nullable=True
    )


    audio_path = Column(
        String,
        nullable=False
    )


    language = Column(
        String,
        nullable=True
    )


    transcribed_text = Column(
        String,
        nullable=True
    )


    ai_match_status = Column(
        String,
        default="PENDING_REVIEW"
    )


    therapist_review = Column(
        String,
        nullable=True
    )

    ai_summary = Column(String, nullable=True)

    ai_suggestion = Column(String, nullable=True)

    review_status = Column(String, default="PENDING")

    therapist_comment = Column(String, nullable=True)


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    goal = relationship(
        "Goal"
    )


    parent = relationship(
        "User"
    )