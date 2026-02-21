from app.db.repositories.collections import pokecoins_collection, shop_pokecoins_collection
from app.schemes.pokecoins_scheme import Pokecoins
from app.converters.pokecoins_converter import pokecoins_converter

class PokecoinsRepository:

    @staticmethod
    async def search_pokecoins(field: str, value):
        pokecoins = await pokecoins_collection.find_one({field: value})
        return Pokecoins(**pokecoins_converter(pokecoins)) if pokecoins else None

    @staticmethod
    async def insert_pokecoins(data_pokecoins: dict):
        insert = await pokecoins_collection.insert_one(data_pokecoins)
        return insert.acknowledged