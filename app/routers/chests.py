import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException, Depends
from services.database import chests_collection, pokemon_figure_collection, chest_status_collection
from schemes.chests_scheme import chest_scheme
from helpers.chests_helper import verify_chest_id, search_chest, search_cheststatus
from models.users_model import User
from helpers.users_helper import verify_token
from manager.chests_manager import ChestsManager, RewardChestManager
from bson import ObjectId

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

@router.get("/my_chests", status_code=status.HTTP_202_ACCEPTED)
async def get_cheststatus(user: User = Depends(verify_token)):
    search = await search_cheststatus(user.id)

    chest_status = ChestsManager(search.chest, search.last_generated, search.next_chest)
    chest_status.update_chest_status()
    model = chest_status.model_cheststatus()

    update = await chest_status_collection.update_one({"user_id": ObjectId(user.id)}, {"$set": model.model_dump()})
    if update.modified_count == 0:
        return {"chest_status": search}

    return {"chest_status": model}

@router.post("/chests/{chest_id}/open", status_code=status.HTTP_202_ACCEPTED)
async def open_chest(chest_id: str, user: User = Depends(verify_token)):
    objectid_chest_id = verify_chest_id(chest_id)
    chest = await search_chest("_id", objectid_chest_id)
    if chest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chest not found")

    chest_status = await search_cheststatus(user.id)
    manager = RewardChestManager(chest_status.chest, chest_status.last_generated, chest_status.next_chest, chest.generation)
    reward = await manager.get_reward()
    if reward is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You haven't chests available")
    update = await chest_status_collection.update_one({"user_id": ObjectId(user.id)}, {"$set": {"chest": manager.chest}})
    if update.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update Chest Error")

    insert_pokemon_figure = await pokemon_figure_collection.insert_one({"user_id": ObjectId(user.id), "pokemon_figure": reward})
    if not insert_pokemon_figure.inserted_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insert Pokemon Figure Error")
    return {"pokemon_figure": reward}