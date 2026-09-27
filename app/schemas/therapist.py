from pydantic import BaseModel


class TherapistCreate(BaseModel):
    username: str
    email: str
    password: str
    specialization: str
    experience: str