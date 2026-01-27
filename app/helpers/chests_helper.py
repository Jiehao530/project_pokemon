import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import HTTPException, status
from services.database import chests_collection, chest_status_collection
from models.chests_model import Chest, ChestStatus
from schemes.chests_scheme import chest_scheme, chest_status_scheme
from bson import ObjectId
from datetime import datetime, timedelta
import random

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

async def insert_chest_status(user_id: str):
    data_chest_status = {
            "user_id": ObjectId(user_id),
            "chest": 1,
            "last_generated": datetime.utcnow(),
            "next_chest": datetime.utcnow() + timedelta(hours=4)
        }
    insert_data = await chest_status_collection.insert_one(data_chest_status)
    id = insert_data.inserted_id
    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    chest_status = await chest_status_collection.find_one({"user_id": ObjectId(user_id)})
    return ChestStatus(**chest_status_scheme(chest_status))

async def search_cheststatus(user_id: str):
    chest_status = await chest_status_collection.find_one({"user_id": ObjectId(user_id)})
    if not chest_status:
        status = await insert_chest_status(user_id)
        return status
    return ChestStatus(**chest_status_scheme(chest_status))

def get_pokemon_number(generation: int):
    if generation == 1:
        number = random.randint(1, 151)
        return number
    elif generation == 2:
        number = random.randint(152, 251)
        return number
    elif generation == 3:
        number = random.randint(252, 386)
        return number
    else:
        return None
