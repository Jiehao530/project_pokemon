import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.database import shop_config_collection, shop_items_collection
from manager.shop_manager import ShopManager
from manager.price_manager import PriceManager
from models.shop_model import ShopRefresh
from models.pokemon_model import PokemonFigureShop
from schemes.shop_scheme import shop_config_scheme, shop_items_pokemon_figure_scheme
from helpers.pokemon_helper import get_pokemon_figure_for_shop
from datetime import datetime

async def get_shop_config(field: str, value):
    shop_config = await shop_config_collection.find_one({field: value})
    if not shop_config:
        return None
    config = ShopRefresh(**shop_config_scheme(shop_config))
    shop_manager = ShopManager(config.refresh_at, config.last_refresh, config.refresh_interval_hours)
    refresh = shop_manager.update_shop_refresh()
    data = shop_manager.get_data()
    if refresh:
        await shop_items_collection.delete_many({"expires_at": {"$lte": datetime.utcnow()}})
        await shop_config_collection.update_one({field: value}, {"$set": data})
    return data

async def insert_shop_items_pokemon_figures(number_repetition: int):
    pokemon_figure_list = await get_pokemon_figure_for_shop(number_repetition)
    for pokemon_figure in pokemon_figure_list:
        price_manager = PriceManager(pokemon_figure["rarity"], pokemon_figure["points"])
        total_price = price_manager.calculate_price()
        





async def get_shop_items_pokemon_figure(field: str, value):
    pokemon_figures_list = await shop_items_collection.find({field: value}).to_list(None)
    if not pokemon_figures_list:
        return None
    return [shop_items_pokemon_figure_scheme(pokemon_figure) for pokemon_figure in pokemon_figures_list]