import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pydantic import BaseModel
from datetime import datetime

class ShopStatus(BaseModel):
    last_generated: datetime
    next_shop: datetime

class ShopStatusDB(ShopStatus):
    id: str