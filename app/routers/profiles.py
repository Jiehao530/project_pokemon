import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status
from helpers.profiles_helper import search_profile
from models.profile_model import Profile

router = APIRouter(tags=["Profiles"])

@router.get("/profile/{username}", status_code=status.HTTP_202_ACCEPTED)
@router.get("/profile/", status_code=status.HTTP_202_ACCEPTED)
async def get_profile(username: str):
    profile = await search_profile("username", username)
    