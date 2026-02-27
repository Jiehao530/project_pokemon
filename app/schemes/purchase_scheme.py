from pydantic import BaseModel
from datetime import datetime

class PurchaseResult(BaseModel):
    item_id : str
    user_id: str
    pokecoins_left: int

class Purchase(BaseModel):
    purchase_id: str
    result: PurchaseResult
    user_id: str
    created_at: datetime