import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException
from models.users_model import NewUser, User
from helpers.users_helper import search_user
from datetime import datetime
from services.database import users_collection
from passlib.context import CryptContext

router = APIRouter(tags=["Users"])
crypt = CryptContext(schemes=["bcrypt"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up_user(new_user: NewUser):
    search_email = await search_user("email", new_user.email)
    if isinstance(search_email, User):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email is already in use")
    search_username = await search_user("username", new_user.username)
    if isinstance(search_username, User):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is already in use")
    
    new_user_dict = dict(new_user)
    new_user_dict["password"] = crypt.hash(new_user.password)
    new_user_dict["created_date"] = datetime.utcnow()
    new_user_dict["last_login"] = datetime.utcnow()

    insert_new_user = await users_collection.insert_one(new_user_dict)
    if not insert_new_user.inserted_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user")
    return {"detail": f"The user {new_user.username} has been created successfully"}
