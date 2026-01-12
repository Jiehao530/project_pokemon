import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status
from helpers.profiles_helper import search_profile
from helpers.follow_helper import get_followers_numbers, get_following_numbers

router = APIRouter(tags=["Profiles"])

@router.get("/profile/{username}", status_code=status.HTTP_202_ACCEPTED)
@router.get("/profile/", status_code=status.HTTP_202_ACCEPTED)
async def get_profile(username: str):
    profile = await search_profile("username", username)
    followers = await get_followers_numbers(profile.user_id)
    following = await get_following_numbers(profile.user_id)
    return {
        "profile": profile.model_dump(), 
        "followers": {"number_of_followers": followers}, 
        "following": {"number_of_following": following}
        }
    