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
pokemon_collection = client["pokemon"]
chests_collection = client["chests"]
pokemon_figure_collection = client["pokemon_figure"]
chest_status_collection = client["chest_status"]
pokecoins_collection = client["pokecoins"]
shop_status_collection = client["shop_status"]
shop_pokemon_figures_collection = client["shop_pokemon_figures"]