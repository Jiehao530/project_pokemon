from fastapi import APIRouter, status, Depends
from app.services.pokecoins_service import PokecoinsService
from app.schemes.users_scheme import User
from app.dependencies.auth_depends import get_current_user

router = APIRouter(tags=["Pokécoins"])

@router.get("/pokecoins", status_code=status.HTTP_202_ACCEPTED)
async def get_pokecoins(user: User = Depends(get_current_user)):
    return await PokecoinsService().get_pokecoins(user)