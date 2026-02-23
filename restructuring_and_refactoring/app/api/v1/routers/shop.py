from fastapi import APIRouter, status
from app.services.shop_service import ShopService

router = APIRouter(tags=["Shop"])

@router.get("/shop/shop_config", status_code=status.HTTP_202_ACCEPTED)
async def get_shop_config():
    return await ShopService().get_shop_config("_id", "daily_shop")