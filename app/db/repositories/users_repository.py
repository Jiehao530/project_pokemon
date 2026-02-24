from app.db.repositories.collections import users_collection
from app.schemes.users_scheme import User
from app.converters.users_converter import user_converter, user_visual_profile_converter, user_id_converter
from datetime import datetime
from bson.objectid import ObjectId

class UserRepository:

    @staticmethod
    async def search_user(field: str, value):
        user = await users_collection.find_one({field: value})
        return User(**user_converter(user)) if user else None
        
    @staticmethod
    async def insert_new_user(new_user: dict):
        insert = await users_collection.insert_one(new_user)
        return insert.inserted_id

    @staticmethod
    async def update_user(user_id: ObjectId, user_update_data: dict):
        update = await users_collection.update_one({"_id": user_id}, {"$set": user_update_data})
        return update.modified_count
    
    @staticmethod
    async def delete_user(user_id: ObjectId):
        delete = await users_collection.delete_one({"_id": user_id})
        return delete.deleted_count

    @staticmethod
    async def update_last_login(user_id: ObjectId):
        update_last_login = await users_collection.update_one({"_id": user_id}, {"$set": {"last_login": datetime.utcnow()}})
        return update_last_login.modified_count

    @staticmethod
    async def search_user_by_email(email: str, user_id: ObjectId):
        search_email = await users_collection.find_one({"email": email, "_id": {"$ne": user_id}})
        return search_email

    @staticmethod
    async def search_user_by_username(username: str, user_id: ObjectId):
        search_username = await users_collection.find_one({"username": username, "_id": {"$ne": user_id}})
        return search_username
    
    @staticmethod
    async def search_username_list_by_id(users_ids: list):
        search_username_list = await users_collection.find({"_id": {"$in": users_ids}}).to_list(None)
        return [user["username"] for user in search_username_list]

    @staticmethod
    async def search_user_visual_profile_by_id(user_id: ObjectId):
        search_user_by_id = await users_collection.find_one({"_id": user_id})
        return user_visual_profile_converter(search_user_by_id) if search_user_by_id else None
    
    @staticmethod
    async def search_user_id_by_username(username: str):
        search_user_id = await users_collection.find_one({"username": username})
        return user_id_converter(search_user_id) if search_user_id else None