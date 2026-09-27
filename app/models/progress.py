from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from datetime import datetime

from app.database.base import Base



class GoalProgress(Base):

    __tablename__ = "goal_progress"


    id = Column(
        Integer,
        primary_key=True
    )


    goal_id = Column(
        Integer,
        ForeignKey(
            "goals.id"
        ),
        nullable=False
    )


    milestone_id = Column(
        Integer,
        ForeignKey(
            "goal_milestones.id"
        ),
        nullable=False
    )


    updated_by = Column(
        Integer,
        ForeignKey(
            "users.id"
        ),
        nullable=False
    )


    status = Column(
        String,
        default="IN_PROGRESS"
    )


    notes = Column(
        String
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )