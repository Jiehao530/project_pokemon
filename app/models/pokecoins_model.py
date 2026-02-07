import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pydantic import BaseModel
from models.shop_model import Currency

class PokecoinsPack(BaseModel):
    id: str
    amount: int
    price: float
    currency: Currency

class PokeCoins(BaseModel):
    user_id: str
    pokecoins: int