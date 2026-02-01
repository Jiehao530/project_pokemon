from pydantic import BaseModel
from typing import List
from enum import Enum

class Pokemon(BaseModel):
    number: int
    name: str
    type: List[str]
    generation: int

class Rarity(str, Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class PokemonFigure(BaseModel):
    pokemon_figure_id: str
    number: int
    name : str
    type: List[str]
    generation: int
    rarity: str
    points: int

class PokemonFigureForSale(PokemonFigure):
    price: int