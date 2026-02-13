from fastapi import APIRouter, status
from app.services.chests_service import ChestsService

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