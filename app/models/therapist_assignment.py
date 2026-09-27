from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class TherapistAssignment(Base):

    __tablename__ = "therapist_assignments"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    therapist_id = Column(
        Integer,
        ForeignKey("therapists.id")
    )


    child_id = Column(
        Integer,
        ForeignKey("children.id")
    )


    therapist = relationship(
        "Therapist",
        back_populates="assignments"
    )


    child = relationship(
        "Child"
    )