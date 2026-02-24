from pydantic import BaseModel, EmailStr

class NewUser(BaseModel):
    username: str
    password: str
    email: EmailStr