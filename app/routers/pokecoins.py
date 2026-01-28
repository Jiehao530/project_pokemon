import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, Depends
from models.users_model import User
from helpers.users_helper import verify_token
from helpers.pokecoins_helper import search_pokecoins
from bson import ObjectId

router = APIRouter(tags=["Pokécoins"])

@router.get("/pokecoins", status_code=status.HTTP_202_ACCEPTED)
async def get_pokecoins(user: User = Depends(verify_token)):
    pokecoins = await search_pokecoins("user_id", ObjectId(user.id))
    return pokecoins