from pydantic import BaseModel


class AssessmentSessionCreate(BaseModel):

    assessment_id: int

    child_id: int



class AssessmentSessionResponse(BaseModel):

    id: int

    assessment_id: int

    child_id: int

    therapist_id: int | None

    status: str


    class Config:
        from_attributes = True