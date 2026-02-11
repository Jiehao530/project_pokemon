from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: str
    username: str
    password: str
    email: EmailStr
    created_date: datetime
    last_login: datetime

class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None