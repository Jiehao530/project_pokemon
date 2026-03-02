from fastapi import APIRouter, status, Depends
from app.services.shop_service import ShopService
from app.schemes.users_scheme import User
from app.dependencies.auth_depends import get_current_user

router = APIRouter(tags=["Shop"])

@router.get("/shop/daily_shop", status_code=status.HTTP_202_ACCEPTED)
async def get_daily_shop():
    return await ShopService().get_daily_shop()

@router.get("/shop/daily_shop/shop_config", status_code=status.HTTP_202_ACCEPTED)
async def get_shop_config():
    return await ShopService().get_shop_config("_id", "daily_shop")

@router.get("/shop/daily_shop/pokecoins_packs", status_code=status.HTTP_202_ACCEPTED)
async def get_pokecoins_packs():
    return await ShopService().get_pokecoins_packs()

@router.get("/shop/daily_shop/pokemon_figures", status_code=status.HTTP_202_ACCEPTED)
async def get_pokemon_figures_for_shop():
    return await ShopService().get_pokemon_figures_for_shop()

@router.get("/shop/daily_shop/item/{item_id}/buy", status_code=status.HTTP_202_ACCEPTED)
async def buy_item_of_the_daily_shop(item_id: str, purchase_id: str, user: User = Depends(get_current_user)):
    return await ShopService().buy_item_of_the_daily_shop(item_id, purchase_id, user)