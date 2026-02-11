import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()
MONGO_CONNECTION = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_CONNECTION)["pokemon_project"]