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
async def get_your_pokemon_figures(page: int = Query(1, ge=1), pagesize: int = Query(24, ge=1, le=48), user: User = Depends(verify_token)):
    total_pokemon_figures = await pokemon_figure_collection.count_documents({"user_id": ObjectId(user.id)})
    
    skip = (page - 1) * pagesize
    pokemon_figures = await pokemon_figure_collection.find({"user_id": ObjectId(user.id)}).skip(skip).limit(pagesize).to_list()
    if not pokemon_figures:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    list_pokemon_figures = [pokemon_figure_scheme(pokemon_figure) for pokemon_figure in pokemon_figures]
    
    return {
        "pokemon_figures": list_pokemon_figures,
        "page": page,
        "pagesize": pagesize,
        "total": total_pokemon_figures,
        "total_pages": (total_pokemon_figures + pagesize -1) // pagesize
    }