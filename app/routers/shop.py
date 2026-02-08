import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException
from services.database import shop_items_collection, shop_config_collection
from models.shop_model import ShopType
from schemes.shop_scheme import shop_items_pokecoins_scheme, shop_config_scheme
from helpers.shop_helper import get_shop_items_pokemon_figure, get_shop_config
from manager.shop_manager import ShopManager

router = APIRouter(tags=["Shop"])

@router.get("/shop/pokecoins", status_code=status.HTTP_202_ACCEPTED)
async def get_pokecoins_pack():
    pokecoins_pack_list = await shop_items_collection.find({"type": ShopType.POKECOINS.value}).to_list(None)
    return [shop_items_pokecoins_scheme(pokecoins_pack) for pokecoins_pack in pokecoins_pack_list]

@router.get("/shop/pokemon_figures", status_code=status.HTTP_202_ACCEPTED)
async def get_pokemon_figures():
    return await get_shop_items_pokemon_figure("type", ShopType.POKEMON_FIGURE.value)

@router.get("/shop/shop_refresh", status_code=status.HTTP_202_ACCEPTED)
async def get_shop_refresh():
    shop_refresh = await get_shop_config("_id", "daily_shop")
    return shop_refresh
