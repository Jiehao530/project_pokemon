from app.db.repositories.shop_repository import ShopRepository
from app.managers.shop_config_manager import ShopManager

class ShopService:

    async def get_shop_config(self, field: str, value):
        shop_config = await ShopRepository.search_shop_config(field, value)
        if not shop_config:
            return {"shop_config": None}

        shop_config_manager = ShopManager(shop_config.refresh_at, shop_config.last_refresh, shop_config.refresh_interval_hours)
        resfresh = shop_config_manager.update_shop_refresh()
        shop_config = shop_config_manager.get_shop_config()

        if resfresh:
            await ShopRepository.delete_shop_items_for_expire()
            await ShopRepository.update_shop_config(field, value, shop_config)
        return {"shop_config": shop_config}