from pydantic import BaseModel
from datetime import datetime

class Profile(BaseModel):
    user_id: str
    username: str
    created_date: datetime