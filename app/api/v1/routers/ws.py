from fastapi import APIRouter, status, Depends
from app.services.ws_service import WedsocketService
from app.schemes.users_scheme import User
from app.dependencies.auth_depends import get_current_user

router = APIRouter(tags=["Websocket"])

@router.get("/ws/exchange/create/room", status_code=status.HTTP_201_CREATED)
async def create_exchange_room(user: User = Depends(get_current_user)):
    await WedsocketService().create_exchange_room(user)