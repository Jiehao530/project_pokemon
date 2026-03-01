from pydantic import BaseModel
from datetime import datetime
from app.enums.currency_enum import Currency

class PurchaseResult(BaseModel):
    item_id : str
    user_id: str
    currency: Currency

class Purchase(BaseModel):
    purchase_id: str
    result: PurchaseResult
    user_id: str
    created_at: datetime