from app.db.repositories.collections import follow_collection
from app.schemes.follow_scheme import Follow
from app.utils.follow_converters import follow_converter

class FollowRepository:

    @staticmethod
    async def search_existing_follow(field_1: str, value_1, field_2: str, value_2):
        follow = await follow_collection.find_one({field_1: value_1, field_2: value_2})
        return Follow(**follow_converter(follow)) if follow else None

    @staticmethod
    async def insert_follow(data_follow: dict):
        insert = await follow_collection.insert_one(data_follow)
        return insert.acknowledged

    @staticmethod
    async def delete_follow(field_1: str, value_1, field_2: str, value_2):
        delete = await follow_collection.delete_one({field_1: value_1, field_2: value_2})
        return delete.deleted_count
    
    @staticmethod
    async def search_follow(field: str, value):
        follow_list = await follow_collection.find({field: value}).to_list(None)
        return [Follow(**follow_converter(follow)) for follow in follow_list] if follow_list else None