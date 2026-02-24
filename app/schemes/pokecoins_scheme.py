from pydantic import BaseModel
from app.enums.currency_enum import Currency

class Pokecoins(BaseModel):
    user_id: str
    amount: int
    currency: Currency

class PokecoinsPack(BaseModel):
    id: str
    amount: int
    price: float
    currency: Currency