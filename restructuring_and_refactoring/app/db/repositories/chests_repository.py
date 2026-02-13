from app.db.repositories.collections import chests_collection
from app.schemes.chests_scheme import Chest
from app.utils.chests_converters import chest_scheme

class ChestsRepository:

    @staticmethod
    async def search_chests():
        chests_list = await chests_collection.find().to_list(None)
        return [Chest(**chest_scheme(chest)) for chest in chests_list] if chests_list else None
    
    @staticmethod
    async def search_chest(field: str, value):
        chest = await chests_collection.find_one({field: value})
        return Chest(**chest_scheme(chest)) if chest else None