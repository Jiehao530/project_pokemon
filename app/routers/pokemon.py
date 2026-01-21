import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException, Depends, Query
from services.database import pokemon_figure_collection
from schemes.pokemon_scheme import pokemon_figure_scheme
from models.users_model import User
from helpers.users_helper import verify_token
from bson import ObjectId


router = APIRouter(tags=["pokémon"])

@router.get("/pokemon_figures", status_code=status.HTTP_202_ACCEPTED)
async def get_your_pokemon_figures(user: User = Depends(verify_token)):
    pokemon_figures_list = await pokemon_figure_collection.find({"user_id": ObjectId(user.id)}).to_list()
    if not pokemon_figures_list:
        return []
    return [pokemon_figure_scheme(pokemon_figure) for pokemon_figure in pokemon_figures_list]