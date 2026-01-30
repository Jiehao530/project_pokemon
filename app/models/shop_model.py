import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pydantic import BaseModel
from datetime import datetime
from typing import List
from models.pokemon_model import PokemonFigure

class ShopStatus(BaseModel):
    last_generated: datetime
    next_shop: datetime

class ShopStatusDB(ShopStatus):
    id: str
    
class ShopPokemonFigures(BaseModel):
    shop_id: str
    shop_name: str
    pokemon_figures: List[PokemonFigure]