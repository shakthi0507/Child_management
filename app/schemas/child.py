from datetime import date

from pydantic import BaseModel


class ChildCreate(BaseModel):

    name: str

    dob: date | None = None

    gender: str | None = None

    height: int | None = None

    weight: int | None = None



class ChildResponse(BaseModel):

    id: int

    child_code: str

    name: str

    dob: date | None

    gender: str | None

    height: int | None

    weight: int | None


    class Config:

        from_attributes = True