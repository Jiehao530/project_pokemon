import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException, Depends
from helpers.follow_helper import verify_follow, search_follow
from helpers.users_helper import verify_token
from models.follow_model import Follow
from models.users_model import User
from services.database import follow_collection
from bson import ObjectId

router = APIRouter(tags=["follow"])

@router.post("/profile/{followed_id}/follow", status_code=status.HTTP_202_ACCEPTED)
async def follow_user(followed_id: str, user: User = Depends(verify_token)):
    search = await verify_follow("follower_id", ObjectId(user.id), "followed_id", ObjectId(followed_id))
    if isinstance(search, Follow):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already following this user")
    
    follow_data = {
        "follower_id": ObjectId(user.id),
        "followed_id": ObjectId(followed_id)
    }
    insert_follow_data = await follow_collection.insert_one(follow_data)
    if not insert_follow_data.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Follow Error")
    return {"detail": f"Followed"}

@router.delete("/profile/{unfollow_id}/unfollow", status_code=status.HTTP_202_ACCEPTED)
async def unfollow_user(unfollow_id: str, user: User = Depends(verify_token)):
    search = await verify_follow("follower_id", ObjectId(user.id), "followed_id", ObjectId(unfollow_id))
    if not isinstance(search, Follow):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You aren't following this user")

    unfollow = await follow_collection.delete_one({"follower_id": ObjectId(user.id), "followed_id": ObjectId(unfollow_id)})
    if unfollow.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unfollow Error")
    return {"detail": f"Unfollowed"}

@router.get("/profile/{user_id}/followers", status_code=status.HTTP_202_ACCEPTED)
async def get_followers(user_id: str):
    search = await search_follow("followed_id", ObjectId(user_id))
    if search is None:
        return []
    return [follower["follower_id"] for follower in search]

@router.get("/profile/{user_id}/following", status_code=status.HTTP_202_ACCEPTED)
async def get_following(user_id: str):
    search = await search_follow("follower_id", ObjectId(user_id))
    if search is None:
        return []
    return [following["followed_id"] for following in search]