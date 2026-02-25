from app.db.repositories.shop_repository import ShopRepository
from app.managers.shop_config_manager import ShopManager
from app.enums.shop_type_enum import ShopType
from app.services.pokemon_figure_service import PokemonFigureService

class ShopService:

    async def get_shop_config(self, field: str, value):
        shop_config = await ShopRepository.search_shop_config(field, value)
        if not shop_config:
            return {"shop_config": "None"}

        shop_config_manager = ShopManager(shop_config.refresh_at, shop_config.last_refresh, shop_config.refresh_interval_hours)
        resfresh = shop_config_manager.update_shop_refresh()
        shop_config = shop_config_manager.get_shop_config()

        if resfresh:
            await ShopRepository.delete_shop_items_for_expire()
            await ShopRepository.update_shop_config(field, value, shop_config)
            await PokemonFigureService().new_pokemon_figures_for_shop(shop_config["refresh_at"])
        return {"shop_config": shop_config}
    
    async def get_pokecoins_packs(self):
        pokecoins_packs_list = await ShopRepository.search_pokecoins_packs_of_the_shop_items("type", ShopType.POKECOINS.value)
        if not pokecoins_packs_list:
            return {"pokecoins_packs": "None"}
        return {"pokecoins_packs": pokecoins_packs_list}

    async def get_pokemon_figures_for_shop(self):
        pokemon_figures_for_shop_list = await ShopRepository.search_pokemon_figures_of_the_shop_items("type", ShopType.POKEMON_FIGURE.value)
        if not pokemon_figures_for_shop_list:
            return {"pokemon_figures": "None"}
        return {"pokemon_figures": pokemon_figures_for_shop_list}

    async def get_daily_shop(self):
        shop_config = await self.get_shop_config("_id", "daily_shop")
        pokemon_figures = await self.get_pokemon_figures_for_shop()
        pokecoins_packs = await self.get_pokecoins_packs()

        return [
            shop_config, 
            pokemon_figures, 
            pokecoins_packs
            ]