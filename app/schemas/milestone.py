from pydantic import BaseModel



class MilestoneCreate(BaseModel):

    age_group: str

    expected_month: int

    domain: str

    title: str

    description: str | None = None