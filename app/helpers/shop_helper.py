import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import HTTPException, status
from services.database import shop_items_collection
from schemes.shop_scheme import shop_items_pokemon_figure_scheme

async def get_shop_items_pokemon_figure(field: str, value):
    pokemon_figures_list = await shop_items_collection.find({field: value}).to_list(None)
    if not pokemon_figures_list:
        return None
    return [shop_items_pokemon_figure_scheme(pokemon_figure) for pokemon_figure in pokemon_figures_list]