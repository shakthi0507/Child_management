from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database.base import Base



class GoalMilestone(Base):

    __tablename__ = "goal_milestones"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    goal_id = Column(
        Integer,
        ForeignKey(
            "goals.id"
        ),
        nullable=False
    )


    title = Column(
        String,
        nullable=False
    )


    description = Column(
        String,
        nullable=True
    )


    # PENDING
    # IN_PROGRESS
    # COMPLETED

    status = Column(
        String,
        default="PENDING"
    )


    target_date = Column(
        DateTime,
        nullable=True
    )


    completed_date = Column(
        DateTime,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    goal = relationship(
        "Goal",
        back_populates="milestones"
    )