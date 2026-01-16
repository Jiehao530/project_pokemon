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
    weights = [50, 35, 10, 5]
    rarity = random.choices(rarity_options, weights=weights, k=1)[0]
    point = random.randint(1, 5)
    return [rarity, point]




    