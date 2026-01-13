import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException
from models.profile_model import Profile
from helpers.users_helper import verify_user_id
from helpers.profiles_helper import search_profile
from helpers.follow_helper import get_followers_numbers, get_following_numbers
router = APIRouter(tags=["Profiles"])

@router.get("/profile/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_profile(user_id: str):
    objectid_user_id = await verify_user_id(user_id)
    profile = await search_profile("user_id", objectid_user_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        
    followers = await get_followers_numbers(profile.user_id)
    following = await get_following_numbers(profile.user_id)
    return {
        "profile": profile.model_dump(), 
        "followers": {"number_of_followers": followers}, 
        "following": {"number_of_following": following}
        }
    