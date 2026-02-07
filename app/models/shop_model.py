import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from models.pokemon_model import PokemonFigureShop

class ShopType(str, Enum):
    POKEMON_FIGURE = "pokemon_figure"
    POKECOINS = "pokecoins"

class Currency(str, Enum):
    POKECOINS = "pokecoins"
    REAL_MONEY = "real_money"

class ShopStatus(BaseModel):
    last_generated: datetime
    next_shop: datetime

class ShopStatusDB(ShopStatus):
    id: str

class ShopPokemonFigures(BaseModel):
    id: str
    type: ShopType
    pokemon_figure: PokemonFigureShop
    price: int
    currency: Currency
    expires_at: datetime

class ShopPokecoins(BaseModel):
    id: str
    type: ShopType
    item_id: str
    price: float
    currency: Currency
