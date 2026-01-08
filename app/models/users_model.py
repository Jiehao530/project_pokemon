from pydantic import BaseModel, EmailStr
from datetime import datetime

class NewUser(BaseModel):
    username: str
    password: str
    email: EmailStr

class User(BaseModel):
    id: str
    username: str
    password: str
    email: EmailStr
    created_date: datetime
    last_login: datetime