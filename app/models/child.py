from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class Child(Base):

    __tablename__ = "children"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    child_code = Column(
        String,
        unique=True,
        nullable=False
    )


    parent_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    name = Column(
        String,
        nullable=False
    )


    dob = Column(
        Date
    )


    gender = Column(
        String
    )


    height = Column(
        Integer
    )


    weight = Column(
        Integer
    )



    parent = relationship(
        "User",
        backref="children"
    )


    assessments = relationship(
    "AssessmentSession",
    back_populates="child"
    )


    development_profiles = relationship(
    "ChildDevelopmentProfile",
    back_populates="child"
    )


    goals = relationship(
        "Goal",
        back_populates="child",
        cascade="all, delete"
    )