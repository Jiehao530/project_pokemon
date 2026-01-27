from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

class Chest(BaseModel):
    name: str
    generation: int

class ChestStatus(BaseModel):
    chest: int
    last_generated: datetime
    next_chest: Optional[datetime] = None