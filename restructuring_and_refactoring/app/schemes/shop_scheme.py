from pydantic import BaseModel
from datetime import datetime
from app.enums.shop_type_enum import ShopType
from app.enums.currency_enum import Currency

class ShopConfig(BaseModel):
    id: str
    refresh_at: datetime
    last_refresh: datetime
    refresh_interval_hours: int

class ShopPokecoinsPack(BaseModel):
    id: str
    type: ShopType
    item_id: str
    price: float
    currency: Currency