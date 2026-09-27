from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base



class AssessmentQuestion(Base):

    __tablename__ = "assessment_questions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    assessment_id = Column(
        Integer,
        ForeignKey(
            "assessments.id"
        ),
        nullable=False
    )


    milestone_id = Column(
        Integer,
        ForeignKey(
            "milestones.id"
        ),
        nullable=False
    )


    question = Column(
        String,
        nullable=False
    )


    order = Column(
        Integer,
        default=0
    )



    assessment = relationship(
        "Assessment",
        back_populates="questions"
    )


    milestone = relationship(
        "Milestone"
    )