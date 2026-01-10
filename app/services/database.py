import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

load_dotenv(env_path)
MONGO_CONNECTION = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_CONNECTION)["pokemon_project"]
users_collection = client["users"]
token_collection = client["tokens"]
profile_collection = client["profiles"]
follow_collection = client["follow"]