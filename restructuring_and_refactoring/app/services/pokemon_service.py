from fastapi import HTTPException, status
from app.db.repositories.pokemon_repository import PokemonRepository
import random

class PokemonService:

    async def get_pokemon_by_chest_generation(generation_number: int):
        if generation_number == 1:
            number = random.randint(1, 151)
        elif generation_number == 2:
            number = random.randint(152, 251)
        elif generation_number == 3:
            number = random.randint(252, 386)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chest Generation not found")
        
        pokemon = await PokemonRepository.search_pokemon("number", number)
        if not pokemon:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemón not found")
        return pokemon