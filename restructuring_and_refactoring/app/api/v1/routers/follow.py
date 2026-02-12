from fastapi import APIRouter, status, Depends
from app.services.follow_service import FollowService
from app.schemes.users_scheme import User
from app.dependencies.auth_depends import get_current_user

router = APIRouter(tags=["follow"])

@router.post("/profile/{followed_id}/follow", status_code=status.HTTP_202_ACCEPTED)
async def follow_user(followed_id: str, user: User = Depends(get_current_user)):
    return await FollowService().follow_user(followed_id, user)

@router.delete("/profile/{unfollow_id}/unfollow", status_code=status.HTTP_202_ACCEPTED)
async def unfollow_user(unfollow_id: str, user: User = Depends(get_current_user)):
    return await FollowService().unfollow_user(unfollow_id, user)

@router.get("/profile/{user_id}/followers", status_code=status.HTTP_202_ACCEPTED)
async def get_followers(user_id: str):
    return await FollowService().get_followers(user_id)

@router.get("/profile/{user_id}/following", status_code=status.HTTP_202_ACCEPTED)
async def get_following(user_id: str):
    return await FollowService().get_following(user_id)

