import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import HTTPException, status
from services.database import pokecoins_collection, shop_pokecoins_collection
from models.pokecoins_model import PokeCoins, PokecoinsPack
from schemes.pokecoins_scheme import pokecoins_scheme, pokecoins_pack_scheme

async def insert_data_pokecoins(user_id):
    data_pokecoins = {
        "user_id": user_id,
        "pokecoins": 100
    }
    insert_data = await pokecoins_collection.insert_one(data_pokecoins) 
    id = insert_data.inserted_id
    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    pokecoins = await pokecoins_collection.find_one({"user_id": user_id})
    return PokeCoins(**pokecoins_scheme(pokecoins))

async def search_pokecoins(field: str, value):
    pokecoins = await pokecoins_collection.find_one({field: value})
    if not pokecoins:
        new = await insert_data_pokecoins(value)
        return new
    return PokeCoins(**pokecoins_scheme(pokecoins))

async def search_pokecoins_pack(field: str, value):
    pokecoins_pack = await shop_pokecoins_collection.find_one({field: value})
    if not pokecoins_pack:
        return None
    return PokecoinsPack(**pokecoins_pack_scheme(pokecoins_pack))