from datetime import datetime

from pydantic import BaseModel



class ProgressCreate(BaseModel):

    goal_id: int

    milestone_id: int

    status: str

    notes: str | None = None





class ProgressResponse(BaseModel):

    id: int

    goal_id: int

    milestone_id: int

    updated_by: int

    status: str

    notes: str | None

    created_at: datetime



    class Config:

        from_attributes = True