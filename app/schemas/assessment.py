from pydantic import BaseModel


class AssessmentCreate(BaseModel):

    name: str

    description: str

    assessment_type: str

    age_group: str

    domain: str