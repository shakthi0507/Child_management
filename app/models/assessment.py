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



class Assessment(Base):

    __tablename__ = "assessments"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String,
        nullable=False
    )


    description = Column(
        String,
        nullable=True
    )


    assessment_type = Column(
        String,
        nullable=False
    )


    age_group = Column(
        String,
        nullable=False
    )


    domain = Column(
        String,
        nullable=False
    )


    created_by = Column(
        Integer,
        ForeignKey(
            "users.id"
        ),
        nullable=False
    )


    status = Column(
        String,
        default="DRAFT"
    )


    version = Column(
        Integer,
        default=1
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



    questions = relationship(
        "AssessmentQuestion",
        back_populates="assessment",
        cascade="all, delete"
    )


    sessions = relationship(
        "AssessmentSession",
        back_populates="assessment"
    )