import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException
from services.database import chests_collection
from schemes.chests_scheme import chest_scheme
from helpers.chests_helper import verify_chest_id, search_chest

router = APIRouter(tags=["chests"])

@router.get("/resolve/chest/{chest_name}", status_code=status.HTTP_202_ACCEPTED)
async def get_chest_id(chest_name: str):
    chest = await chests_collection.find_one({"name": chest_name})
    if chest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chest not found")
    return {"chest_id": str(chest["_id"])}

@router.get("/chests", status_code=status.HTTP_202_ACCEPTED)
async def get_chests():
    search_chests = await chests_collection.find().to_list()
    if not search_chests:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There aren't chests")
    chests = [chest_scheme(chest) for chest in search_chests]
    return {"chests": chests}

@router.get("/chests/{chest_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_chest(chest_id: str):
    objectid_chest_id = verify_chest_id(chest_id)
    chest = await search_chest("_id", objectid_chest_id)
    if chest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chest not found")
    return chest