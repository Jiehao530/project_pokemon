import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__), ".."))
from services.database import follow_collection
from models.follow_model import Follow
from schemes.follow_scheme import follow_scheme

async def search_follow(field: str, value, field_2: str, value_2):
    follow = await follow_collection.find_one({field: value, field_2: value_2})
    if not follow:
        return None
    return Follow(**follow_scheme(follow))