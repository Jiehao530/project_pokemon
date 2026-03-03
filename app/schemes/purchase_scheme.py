from pydantic import BaseModel
from datetime import datetime
from app.enums.currency_enum import Currency

class PurchaseRequest(BaseModel):
    purchase_id: str

class PurchaseResult(BaseModel):
    item_id : str
    currency: Currency
    status: int

class Purchase(BaseModel):
    purchase_id: str
    result: PurchaseResult
    user_id: str
    created_at: datetime