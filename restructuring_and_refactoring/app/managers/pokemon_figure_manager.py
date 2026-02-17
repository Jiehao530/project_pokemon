from app.db.repositories.pokemon_repository import PokemonRepository
from app.constants.pokemon_figure_constants import GENERATION_RANGES, RARITY_OPTIONS, POINT_OPTIONS, RARITY_WEIGHTS_FOR_CHESTS, POINT_WEIGHTS_FOR_CHESTS
from bson.objectid import ObjectId
import random

class PokemonFigureManager:

    @staticmethod
    async def get_pokemon_figure_for_chest(chest_generation: int):
        start_num, end_num = GENERATION_RANGES[chest_generation]

        pokemon_number = random.randint(start_num, end_num)
        pokemon = await PokemonRepository.search_pokemon("number", pokemon_number)
        
        rarity = random.choices(RARITY_OPTIONS, weights=RARITY_WEIGHTS_FOR_CHESTS, k=1)[0]
        points = random.choices(POINT_OPTIONS, weights=POINT_WEIGHTS_FOR_CHESTS, k=1)[0]
        
        return {
            "pokemon_figure_id": ObjectId(),
            "number": pokemon.number,
            "name": pokemon.name,
            "type": pokemon.type,
            "generation": pokemon.generation,
            "rarity": rarity,
            "points": points
        }