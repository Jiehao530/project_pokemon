import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

load_dotenv(env_path)
MONGO_CONNECTION = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_CONNECTION)["pokemon_project"]

# USERS
#------------------------------------------------------
users_collection = client["users"]
token_collection = client["tokens"]

# PROFILE
#------------------------------------------------------
profile_collection = client["profiles"]
follow_collection = client["follow"]

# POKÉMON
#------------------------------------------------------
pokemon_collection = client["pokemon"]

# CHESTS
#-----------------------------------------------------
chests_collection = client["chests"]
chest_status_collection = client["chest_status"]

# POKÉMON FIGURE
#-----------------------------------------------------
pokemon_figure_collection = client["pokemon_figure"]

# POKECOINS
#-----------------------------------------------------
pokecoins_collection = client["pokecoins"]

# SHOP
#-----------------------------------------------------
shop_status_collection = client["shop_status"]
shop_items_collection = client["shop_items"]
shop_pokemon_figures_collection = client["shop_pokemon_figures"]
shop_pokecoins_collection = client["shop_pokecoins"]