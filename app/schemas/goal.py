from datetime import datetime

from pydantic import BaseModel



class GoalCreate(BaseModel):

    child_id: int

    therapist_id: int

    assessment_session_id: int | None = None

    domain: str

    current_level: str

    short_term_goal: str

    long_term_goal: str

    duration_days: int

class GoalUpdate(BaseModel):

    short_term_goal: str
    long_term_goal: str
    duration_days: int
    status: str

class GoalResponse(BaseModel):

    id: int

    child_id: int

    therapist_id: int

    domain: str

    current_level: str | None

    short_term_goal: str

    long_term_goal: str

    duration_days: int | None

    status: str

    created_at: datetime


    class Config:
        from_attributes = True