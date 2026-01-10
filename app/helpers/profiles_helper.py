import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__), ".."))
from fastapi import HTTPException, status
from services.database import profile_collection
from models.profile_model import Profile
from schemes.profile_scheme import profile_scheme


async def search_profile(field: str, value):
    profile = await profile_collection.find_one({field: value})
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return Profile(**profile_scheme(profile))
