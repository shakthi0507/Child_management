from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class Therapist(Base):

    __tablename__ = "therapists"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )


    specialization = Column(
        String
    )


    experience = Column(
        String
    )


    user = relationship(
        "User"
    )


    assignments = relationship(
        "TherapistAssignment",
        back_populates="therapist"
    )