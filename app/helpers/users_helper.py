import os
import sys
sys.path.insert(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.database import users_collection
from models.users_model import User
from schemes.users_schemes import user_scheme

async def search_user(field: str, value):
    user = users_collection.find_one({field: value})
    if user:
        return User(**user_scheme(user))
    else:
        return None