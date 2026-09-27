from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class GoalRecommendation(Base):

    __tablename__ = "goal_recommendations"


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


    domain = Column(
        String,
        nullable=False
    )


    priority = Column(
        String,
        nullable=False
    )


    current_level = Column(
        String,
        nullable=False
    )


    development_gap = Column(
        String
    )


    short_term_goal = Column(
        String,
        nullable=False
    )


    long_term_goal = Column(
        String,
        nullable=False
    )


    duration_days = Column(
        Integer,
        default=90
    )


    status = Column(
        String,
        default="PENDING_REVIEW"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    reviewed_by = Column(
        Integer,
        ForeignKey(
            "users.id"
        ),
        nullable=True
    )


    therapist_notes = Column(
        String,
        nullable=True
    )


    reviewed_at = Column(
        DateTime,
        nullable=True
    )