from app.db.repositories.collections import token_collection

class AuthRepository:

    @staticmethod
    async def insert_token(data_token: dict):
        insert = await token_collection.insert_one(data_token)
        return insert.inserted_id
    
    @staticmethod
    async def search_token(field: str, value):
        token = await token_collection.find_one({field: value})
        return token

    @staticmethod
    async def delete_token(field: str, value):
        delete = await token_collection.delete_one({field: value})
        return delete.deleted_count