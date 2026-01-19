import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.database import pokemon_collection
from models.pokemon_model import Pokemon, Rarity
from schemes.pokemon_scheme import pokemon_scheme
import random

async def search_pokemon(number: int):
    pokemon = await pokemon_collection.find_one({"number": number})
    if not pokemon:
        return None
    return Pokemon(**pokemon_scheme(pokemon))

def get_rarity_and_point_pokemon():
    rarity_options = [Rarity.COMMON.value, Rarity.RARE.value, Rarity.EPIC.value, Rarity.LEGENDARY.value]
    rarity_weights = [50, 35, 10, 5]
    rarity = random.choices(rarity_options, weights=rarity_weights, k=1)[0]
    point_options = [1, 2, 3, 4, 5]
    point_weights = [46, 33, 15, 5, 1]
    point = random.choices(point_options, weights=point_weights, k=1)[0]
    return [rarity, point]




    