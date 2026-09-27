from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.database.base import Base
from sqlalchemy.orm import relationship


class AssessmentResponse(Base):

    __tablename__ = "assessment_responses"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session = relationship(
        "AssessmentSession",
        back_populates="responses"
    )


    question = relationship(
        "AssessmentQuestion"
    )

    session_id = Column(
        Integer,
        ForeignKey(
            "assessment_sessions.id"
        ),
        nullable=False
    )


    question_id = Column(
        Integer,
        ForeignKey(
            "assessment_questions.id"
        ),
        nullable=False
    )


    answer = Column(
        String,
        nullable=False
    )


    score = Column(
        Integer,
        nullable=True
    )


    # Only therapist uses this
    therapist_remark = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )