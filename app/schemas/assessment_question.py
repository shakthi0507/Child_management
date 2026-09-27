from pydantic import BaseModel

class AssessmentQuestionCreate(BaseModel):

    assessment_id: int
    question: str