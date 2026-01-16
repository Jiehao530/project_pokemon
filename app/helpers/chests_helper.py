import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import HTTPException, status
from services.database import chests_collection
from models.chests_model import Chest
from schemes.chests_scheme import chest_scheme
from bson import ObjectId

async def search_chest(field: str, value):
    chest = await chests_collection.find_one({field: value})
    if not chest:
        return None
    return Chest(**chest_scheme(chest))

def verify_chest_id(chest_id: str):
    try:
        return ObjectId(chest_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid chest_id")

