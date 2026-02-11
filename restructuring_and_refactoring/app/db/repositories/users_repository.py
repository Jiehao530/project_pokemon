from app.db.repositories.collections import users_collection
from app.schemes.users_scheme import User
from app.utils.users_converters import user_converter
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
    async def update_user(user_id: str, user_update_data: dict):
        update = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_update_data})
        return update.modified_count
    
    @staticmethod
    async def delete_user(user_id: str):
        delete = await users_collection.delete_one({"_id": ObjectId(user_id)})
        return delete.deleted_count

    @staticmethod
    async def update_last_login(user_id: str):
        update_last_login = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"last_login": datetime.utcnow()}})
        return update_last_login.modified_count

    @staticmethod
    async def search_user_by_email(email: str, user_id: str):
        search_email = await users_collection.find_one({"email": email, "_id": {"$ne": ObjectId(user_id)}})
        return search_email

    @staticmethod
    async def search_user_by_username(username: str, user_id: str):
        search_username = await users_collection.find_one({"username": username, "_id": {"$ne": ObjectId(user_id)}})
        return search_username