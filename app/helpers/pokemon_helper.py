import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.database import pokemon_collection
from models.pokemon_model import Pokemon, Rarity
from schemes.pokemon_scheme import pokemon_scheme
from bson import ObjectId
import random

async def search_pokemon(number: int):
    pokemon = await pokemon_collection.find_one({"number": number})
    if not pokemon:
        return None
    return Pokemon(**pokemon_scheme(pokemon))

async def get_pokemon(chest_generation_number: int):
    if chest_generation_number == 1:
        number = random.randint(1, 151)
    elif chest_generation_number == 2:
        number = random.randint(152, 251)
    elif chest_generation_number == 3:
        number = random.randint(252, 386)

    pokemon = await search_pokemon(number)
    return pokemon
    
def get_rarity_and_point_pokemon():
    rarity_options = [Rarity.COMMON.value, Rarity.RARE.value, Rarity.EPIC.value, Rarity.LEGENDARY.value]
    rarity_weights = [50, 35, 10, 5]
    rarity = random.choices(rarity_options, weights=rarity_weights, k=1)[0]
    point_options = [1, 2, 3, 4, 5]
    point_weights = [46, 33, 15, 5, 1]
    point = random.choices(point_options, weights=point_weights, k=1)[0]
    return [rarity, point]

async def get_pokemon_figure_by_chest(generation: int):
    pokemon = await get_pokemon(generation)
    rarity, points = get_rarity_and_point_pokemon()
    return {
            "pokemon_figure_id": ObjectId(),
            "number": pokemon.number,
            "name": pokemon.name,
            "type": pokemon.type,
            "generation": pokemon.generation,
            "rarity": rarity,
            "points": points
        }

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

async def get_pokemon_figure_for_shop(number_repetition: int):
    pokemon_figures = []
    
    for _ in range(number_repetition):
        pokemon = None
        while pokemon is None:
            number = random.randint(1, 151)
            pokemon = await search_pokemon(number)
        rarity, points =  get_rarity_and_point_pokemon()
        pokemon_figure = {
            "number": pokemon.number,
            "name": pokemon.name,
            "type": pokemon.type,
            "generation": pokemon.generation,
            "rarity": rarity,
            "points": points
        }
        pokemon_figures.append(pokemon_figure)
    
    return pokemon_figures