from app.db.repositories.collections import pokecoins_collection, shop_pokecoins_collection
from app.schemes.pokecoins_scheme import Pokecoins, PokecoinsPack
from app.converters.pokecoins_converter import pokecoins_converter, pokecoins_pack_converter

class PokecoinsRepository:

    @staticmethod
    async def search_pokecoins(field: str, value):
        pokecoins = await pokecoins_collection.find_one({field: value})
        return Pokecoins(**pokecoins_converter(pokecoins)) if pokecoins else None

    @staticmethod
    async def insert_pokecoins(data_pokecoins: dict):
        insert = await pokecoins_collection.insert_one(data_pokecoins)
        return insert.acknowledged

    @staticmethod
    async def update_pokecoins_amount(field: str, value, pokecoins: int):
        update = await pokecoins_collection.update_one({field: value}, {"$inc": {"amount": pokecoins}})
        return update.acknowledged

    @staticmethod
    async def search_pokecoins_pack(field: str, value):
        pokecoins_pack = await shop_pokecoins_collection.find_one({field: value})
        return PokecoinsPack(**pokecoins_pack_converter(pokecoins_pack)) if pokecoins_pack else None