import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status
from helpers.shop_helper import get_normal_shop_status, search_shop_pokemon_figures
from schemes.pokemon_scheme import pokemon_figure_for_sale_scheme

router = APIRouter(tags=["Shop"])

@router.get("/shop", status_code=status.HTTP_202_ACCEPTED)
async def get_shop():
    shop_status = await get_normal_shop_status("normal_shop")
    shop_pokemon_figure = await search_shop_pokemon_figures("shop_name", "normal_shop")
    return {
        "shop_status": shop_status.next_shop,
        "pokemon_figures": [pokemon_figure_for_sale_scheme(pokemon_figure.model_dump()) for pokemon_figure in shop_pokemon_figure.pokemon_figures]
        }