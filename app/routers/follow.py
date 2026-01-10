import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException, Depends
from helpers.users_helper import verify_token
from models.users_model import User
from services.database import follow_collection
from bson import ObjectId

router = APIRouter(tags=["follow"])

@router.post("/profile/{followed_id}/follow", status_code=status.HTTP_202_ACCEPTED)
async def follow_user(followed_id: str, user: User = Depends(verify_token)):
    follow_data = {
        "follower_id": ObjectId(user.id),
        "followed_id": ObjectId(followed_id)
    }
    insert_follow_data = await follow_collection.insert_one(follow_data)
    if not insert_follow_data.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Follow Error")
    return {"detail": f"Followed"}