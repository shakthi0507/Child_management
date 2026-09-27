from datetime import datetime

from pydantic import BaseModel


class GoalMilestoneCreate(BaseModel):

    goal_id: int

    title: str



class GoalMilestoneResponse(BaseModel):

    id: int

    goal_id: int

    title: str

    status: str
    target_date: datetime | None = None
    completed_date: datetime | None = None


    class Config:

        from_attributes = True