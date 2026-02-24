from fastapi import APIRouter, status, Depends
from app.services.chests_service import ChestsService
from app.schemes.users_scheme import User
from app.dependencies.auth_depends import get_current_user

router = APIRouter(tags=["chests"])

@router.get("/resolve/chest/{chest_name}", status_code=status.HTTP_202_ACCEPTED)
async def get_chest_id(chest_name: str):
    return await ChestsService().get_chest_id(chest_name)

@router.get("/chests", status_code=status.HTTP_202_ACCEPTED)
async def get_chests():
    return await ChestsService().get_chests()

@router.get("/chests/{chest_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_chest(chest_id: str):
    return await ChestsService().get_chest(chest_id)

@router.get("/my_chests", status_code=status.HTTP_202_ACCEPTED)
async def get_cheststatus(user: User = Depends(get_current_user)):
    return await ChestsService().get_cheststatus(user)

@router.post("/chests/{chest_id}/open", status_code=status.HTTP_202_ACCEPTED)
async def open_chest(chest_id: str, user: User = Depends(get_current_user)):
    return await ChestsService().open_chest(chest_id, user)