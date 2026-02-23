from app.db.repositories.collections import shop_config_collection, shop_items_collection
from app.schemes.shop_scheme import ShopConfig, ShopPokecoinsPack
from app.converters.shop_converter import shop_config_converter, shop_items_pokecoins_pack_converter
from datetime import datetime

class ShopRepository:

    @staticmethod
    async def search_shop_config(field: str, value):
        shop_config = await shop_config_collection.find_one({field: value})
        return ShopConfig(**shop_config_converter(shop_config)) if shop_config else None
    
    @staticmethod
    async def update_shop_config(field: str, value, shop_config_update_data: dict):
        update = await shop_config_collection.update_one({field: value}, {"$set": shop_config_update_data})
        return update.acknowledged
    
    @staticmethod
    async def delete_shop_items_for_expire():
        delete = await shop_items_collection.delete_many({"expires_at": {"$lte": datetime.utcnow()}})
        return delete.acknowledged

    @staticmethod
    async def search_pokecoins_packs_of_the_shop_items(field: str, value):
        pokecoins_packs_list = await shop_items_collection.find({field: value}).to_list(None)
        return [
            ShopPokecoinsPack(**shop_items_pokecoins_pack_converter(pokecoins_pack)) 
            for pokecoins_pack in pokecoins_packs_list
            ] if pokecoins_packs_list else None