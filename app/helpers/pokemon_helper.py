import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.database import pokemon_collection
from models.pokemon_model import Pokemon
from schemes.pokemon_scheme import pokemon_scheme
from bson import ObjectId

async def search_pokemon(number: int):
    pokemon = await pokemon_collection.find_one({"number": number})
    if not pokemon:
        return None
    return Pokemon(**pokemon_scheme(pokemon))

def get_search_parameters(user_id: str, number, name, type, generation, rarity, points):
    search_parameters = {"user_id": ObjectId(user_id)}

    if number is not None:
        search_parameters["pokemon_figure.number"] = number
    if name is not None:
        search_parameters["pokemon_figure.type"] = name
    if type is not None:
        search_parameters["pokemon_figure.type"] = {"$in": type}
    if generation is not None:
        search_parameters["pokemon_figure.generation"] = generation
    if rarity is not None:
        search_parameters["pokemon_figure.rarity"] = rarity
    if points is not None:
        search_parameters["pokemon_figure.points"] = points
    
    return search_parameters