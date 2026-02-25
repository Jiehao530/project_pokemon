from fastapi import APIRouter, status
from app.services.shop_service import ShopService

router = APIRouter(tags=["Shop"])

@router.get("/shop/daily_shop", status_code=status.HTTP_202_ACCEPTED)
async def get_daily_shop():
    return await ShopService().get_daily_shop()

@router.get("/shop/shop_config", status_code=status.HTTP_202_ACCEPTED)
async def get_shop_config():
    return await ShopService().get_shop_config("_id", "daily_shop")

@router.get("/shop/pokecoins_packs", status_code=status.HTTP_202_ACCEPTED)
async def get_pokecoins_packs():
    return await ShopService().get_pokecoins_packs()

@router.get("/shop/pokemon_figures", status_code=status.HTTP_202_ACCEPTED)
async def get_pokemon_figures_for_shop():
    return await ShopService().get_pokemon_figures_for_shop()