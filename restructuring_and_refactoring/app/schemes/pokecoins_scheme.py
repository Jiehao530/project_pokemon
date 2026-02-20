from pydantic import BaseModel

class PokeCoins(BaseModel):
    user_id: str
    amount: int
    currency: str