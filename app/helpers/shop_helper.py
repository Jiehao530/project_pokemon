import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import HTTPException, status
from services.database import shop_status_collection, shop_pokemon_figures_collection
from helpers.pokemon_helper import search_pokemon, get_rarity_and_point_pokemon, get_price_for_pokemon_figure
from models.shop_model import ShopStatusDB, ShopPokemonFigures
from schemes.shop_scheme import shop_status_scheme, shop_pokemon_figures_scheme
from manager.shop_manager import ShopManager
from bson import ObjectId
import random

async def get_pokemon_figure_for_shop(number_repetition: int):
    pokemon_figures = []
    
    for _ in range(number_repetition):
        pokemon = None
        while pokemon is None:
            number = random.randint(1, 151)
            pokemon = await search_pokemon(number)
        rarity, points =  get_rarity_and_point_pokemon()
        price = get_price_for_pokemon_figure(rarity, points)
        pokemon_figure = {
            "pokemon_figure_id": ObjectId(),
            "number": pokemon.number,
            "name": pokemon.name,
            "type": pokemon.type,
            "generation": pokemon.generation,
            "rarity": rarity,
            "points": points,
            "price": price
        }
        pokemon_figures.append(pokemon_figure)
    
    return pokemon_figures

async def search_shop_status(field: str, value):
    shop_status = await shop_status_collection.find_one({field: value})
    if not shop_status:
        return None
    return ShopStatusDB(**shop_status_scheme(shop_status))

async def search_shop_pokemon_figures(field: str, value):
    shop_pokemon_figures = await shop_pokemon_figures_collection.find_one({field: value})
    if not shop_pokemon_figures:
        return None
    return ShopPokemonFigures(**shop_pokemon_figures_scheme(shop_pokemon_figures))

async def update_pokemon_figures_for_shop(number_repetition: int, shop_id: str):
    new_pokemon_figures = await get_pokemon_figure_for_shop(number_repetition)
    update_data = {
        "pokemon_figures": new_pokemon_figures
    }
    await shop_pokemon_figures_collection.update_one({"shop_id": ObjectId(shop_id)}, {"$set": update_data})

async def get_normal_shop_status(shop_name: str):
    shop_status = await search_shop_status("name", shop_name)
    if shop_status is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop Status not found")
        
    normal_shop = ShopManager(shop_status.last_generated, shop_status.next_shop)
    update_data = normal_shop.update_shop_status()
    model = model = normal_shop.model_shop_status()

    if update_data:
        await shop_status_collection.update_one({"name": shop_name}, {"$set": model.model_dump()})
        await update_pokemon_figures_for_shop(3, shop_status.id)
    
    return model