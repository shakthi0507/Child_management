from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database.base import Base



class Goal(Base):

    __tablename__ = "goals"


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


    therapist_id = Column(
        Integer,
        ForeignKey(
            "users.id"
        ),
        nullable=False
    )

    assessment_session_id = Column(
        Integer,
        ForeignKey("assessment_sessions.id"),
        nullable=True
    )


    # Speech & Language
    # Motor
    # Cognition
    # Social
    # Behaviour
    # Self-help

    domain = Column(
        String,
        nullable=False
    )


    # Example:
    # 24 months

    current_level = Column(
        String,
        nullable=True
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
        nullable=False
    )


    status = Column(
        String,
        default="ACTIVE"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    child = relationship(
        "Child"
    )


    therapist = relationship(
        "User"
    )


    milestones = relationship(
        "GoalMilestone",
        back_populates="goal",
        cascade="all, delete"
    )