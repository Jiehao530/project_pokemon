from fastapi import APIRouter, status
from app.services.profiles_service import ProfileService

router = APIRouter(tags=["Profiles"])

@router.get("/profile/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_profile(user_id: str):
    return await ProfileService().get_profile(user_id)