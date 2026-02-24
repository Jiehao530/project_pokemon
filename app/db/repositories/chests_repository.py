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

    @staticmethod
    async def search_chest_status(field: str, value):
        cheststatus = await chest_status_collection.find_one({field: value})
        return ChestStatusDB(**chest_status_database_converter(cheststatus)) if cheststatus else None

    @staticmethod
    async def insert_chest_status(data_chest_status: dict):
        insert = await chest_status_collection.insert_one(data_chest_status)
        return insert.acknowledged
    
    @staticmethod
    async def update_chest_status(user_id: ObjectId, update_data: dict):
        update = await chest_status_collection.update_one({"user_id": user_id}, {"$set": update_data})
        return update.acknowledged