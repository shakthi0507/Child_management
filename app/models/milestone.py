from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.database.base import Base


class Milestone(Base):

    __tablename__ = "milestones"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    age_group = Column(
        String,
        nullable=False
    )


    expected_month = Column(
        Integer,
        nullable=False
    )


    domain = Column(
        String,
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