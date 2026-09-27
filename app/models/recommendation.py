from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class Recommendation(Base):

    __tablename__ = "recommendations"


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


    profile_id = Column(
        Integer,
        ForeignKey(
            "child_development_profiles.id"
        ),
        nullable=False
    )


    domain = Column(
        String,
        nullable=False
    )


    recommendation = Column(
        String,
        nullable=False
    )


    reason = Column(
        String,
        nullable=True
    )


    status = Column(
        String,
        default="PENDING"
    )


    therapist_note = Column(
        String,
        nullable=True
    )


    created_by = Column(
        String,
        default="AI"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )