from fastapi import APIRouter, status, Depends, Query
from app.services.pokemon_figure_service import PokemonFigureService
from app.schemes.users_scheme import User
from app.dependencies.auth_depends import get_current_user
from typing import Optional, List

router = APIRouter(tags=["Pokémon Figures"])

@router.get("/pokemon_figures", status_code=status.HTTP_202_ACCEPTED)
async def get_your_pokemon_figures(
    page: int = Query(1, ge=1, description="Obligation"), 
    pagesize: int = Query(24, ge=1, le=48, description="Obligation"),
    number: Optional[int] = Query(None, ge=1, description="Optional"),
    name: Optional[str] = Query(None, description="Optional"),
    type: Optional[List[str]] = Query(None, description="Optional"),
    generation: Optional[int] = Query(None, ge=1, le=3, description="Optional"),
    rarity: Optional[str] = Query(None, description="Optional"),
    points: Optional[int] = Query(None, ge=1, le=5, description="Optional"),
    user: User = Depends(get_current_user)
    ):
    return await PokemonFigureService().get_your_pokemon_figures(
        user.id, number, name, type, generation, rarity, points, page, pagesize)