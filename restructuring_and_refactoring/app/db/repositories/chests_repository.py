from app.db.repositories.collections import chests_collection, chest_status_collection
from app.schemes.chests_scheme import Chest, ChestStatusDB
from app.converters.chests_converter import chest_converter, chest_status_database_converter
from bson.objectid import ObjectId

class ChestsRepository:

    @staticmethod
    async def search_chests():
        chests_list = await chests_collection.find().to_list(None)
        return [Chest(**chest_converter(chest)) for chest in chests_list] if chests_list else None
    
    @staticmethod
    async def search_chest(field: str, value):
        chest = await chests_collection.find_one({field: value})
        return Chest(**chest_converter(chest)) if chest else None