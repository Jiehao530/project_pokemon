from pydantic import BaseModel
from typing import List
from app.enums.shop_type_enum import ShopType
from app.enums.currency_enum import Currency
from datetime import datetime

class PokemonFigure(BaseModel):
    pokemon_figure_id: str
    number: int
    name: str
    type: List[str]
    generation: int
    rarity: str
    points: int

class PokemonFigureShop(BaseModel):
    number: int
    name: str
    type: List[str]
    generation: int
    rarity: str
    points: int