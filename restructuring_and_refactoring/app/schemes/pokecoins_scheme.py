from pydantic import BaseModel
from app.enums.currency_enum import Currency

class Pokecoins(BaseModel):
    user_id: str
    amount: int
    currency: Currency