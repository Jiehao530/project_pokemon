from fastapi import HTTPException, status
from app.db.repositories.pokecoins_repository import PokecoinsRepository
from app.schemes.users_scheme import User
from app.utils.pokecoins_data import new_pokecoins_data
from app.utils.id_converter import id_converter
from bson.objectid import ObjectId

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

    @staticmethod
    async def buy_pokecoins_pack(item_of_the_shop_items: dict, user: User):
        pokecoins_pack = await PokecoinsRepository.search_pokecoins_pack("_id", item_of_the_shop_items["item_id"])
        if not pokecoins_pack:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokecoins Pack not found")
        
        objectid_user_id = id_converter(user.id)
        increase = await PokecoinsRepository.update_pokecoins_amount("user_id", objectid_user_id, pokecoins_pack.amount)
        if not increase:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Increase Pokecoins Error")
        return True

    async def subtract_pokecoins_for_buying(self, price_of_the_item: int, user: User):
        pokecoins = await self.get_pokecoins(user)
        amount = pokecoins["pokecoins"]
        if price_of_the_item > amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You don't have enough pokecoins")
        update_pokecoins = await PokecoinsRepository.update_pokecoins_amount("user_id", id_converter(user.id), -price_of_the_item)
        if not update_pokecoins:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update Pokecoins Error")
        return True