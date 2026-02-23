from pydantic import BaseModel
from datetime import datetime

class ShopConfig(BaseModel):
    id: str
    refresh_at: datetime
    last_refresh: datetime
    refresh_interval_hours: int