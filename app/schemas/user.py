from pydantic import BaseModel



class UserRegister(BaseModel):

    username: str

    email: str

    password: str

    role: str = "PARENT"



class UserLogin(BaseModel):

    email: str

    password: str



class UserResponse(BaseModel):

    id: int

    username: str

    email: str

    role: str

    is_active: bool


    class Config:

        from_attributes = True