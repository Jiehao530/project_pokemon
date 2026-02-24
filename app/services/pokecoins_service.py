from fastapi import HTTPException, status
from app.db.repositories.pokecoins_repository import PokecoinsRepository
from app.schemes.users_scheme import User
from app.utils.pokecoins_data import new_pokecoins_data
from app.utils.id_converter import id_converter

class PokecoinsService:

    async def get_pokecoins(self, user: User):
        objectid_user_id = id_converter(user.id)
        pokecoins = await PokecoinsRepository.search_pokecoins("user_id", objectid_user_id)
        if not pokecoins:
            insert_pokecoins = await PokecoinsRepository.insert_pokecoins(new_pokecoins_data(objectid_user_id))
            if not insert_pokecoins:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insert Pokecoins Error")
            new_pokecoins = await PokecoinsRepository.search_pokecoins("user_id", objectid_user_id)
            return {"pokecoins": new_pokecoins.amount}
        return {"pokecoins": pokecoins.amount}