from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String
)

from datetime import datetime

from app.database.base import Base
from sqlalchemy.orm import relationship


class AssessmentSession(Base):

    __tablename__ = "assessment_sessions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    assessment = relationship(
        "Assessment",
        back_populates="sessions"
    )


    responses = relationship(
        "AssessmentResponse",
        back_populates="session",
        cascade="all, delete"
    )


    child = relationship(
        "Child",
        back_populates="assessments"
    )
    
    assessment_id = Column(
        Integer,
        ForeignKey(
            "assessments.id"
        ),
        nullable=False
    )


    child_id = Column(
        Integer,
        ForeignKey(
            "children.id"
        ),
        nullable=False
    )


    therapist_id = Column(
        Integer,
        ForeignKey(
            "users.id"
        ),
        nullable=True
    )


    # STARTED
    # COMPLETED
    status = Column(
        String,
        default="STARTED"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )