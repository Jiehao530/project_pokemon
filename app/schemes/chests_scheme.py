from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Chest(BaseModel):
    id: str
    name: str
    generation: int

class ChestStatus(BaseModel):
    chest: int
    last_generated: datetime
    next_chest: Optional[datetime] = None

class ChestStatusDB(ChestStatus):
    id: str
    user_id: str