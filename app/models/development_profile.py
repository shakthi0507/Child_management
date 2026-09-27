from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean
)

from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.base import Base


class ChildDevelopmentProfile(Base):

    __tablename__ = "child_development_profiles"


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


    assessment_session_id = Column(
        Integer,
        ForeignKey(
            "assessment_sessions.id"
        ),
        nullable=False
    )

    assessment_session = relationship(
        "AssessmentSession"
    )

    domain = Column(
        String,
        nullable=False
    )


    system_level = Column(
        String,
        nullable=False
    )


    score_percentage = Column(
        Integer,
        nullable=False
    )


    development_gap = Column(
        String,
        nullable=True
    )


    therapist_level = Column(
        String,
        nullable=True
    )


    clinical_interpretation = Column(
        String,
        nullable=True
    )


    confirmed = Column(
        Boolean,
        default=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    child = relationship(
        "Child",
        back_populates="development_profiles"
    )