from pydantic import BaseModel

class AssessmentResponseCreate(BaseModel):

    child_id: int
    question_id: int
    answer: str