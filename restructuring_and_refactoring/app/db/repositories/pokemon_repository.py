from app.db.repositories.collections import pokemon_collection
from app.schemes.pokemon_scheme import Pokemon
from app.converters.pokemon_converter import pokemon_converter

class PokemonRepository:

    @staticmethod
    async def search_pokemon(field: str, value):
        pokemon = await pokemon_collection.find_one({field: value})
        return Pokemon(**pokemon_converter(pokemon)) if pokemon else None