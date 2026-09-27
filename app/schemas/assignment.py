from pydantic import BaseModel


class AssignmentCreate(BaseModel):

    therapist_id: int

    child_id: int