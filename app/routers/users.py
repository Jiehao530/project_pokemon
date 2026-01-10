import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.users_model import NewUser, User
from schemes.users_scheme import user_visual_scheme
from helpers.users_helper import search_user, delete_existing_token, get_token, verify_token, existing_username, id_matching
from datetime import datetime
from services.database import users_collection
from passlib.context import CryptContext
from bson import ObjectId

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
    
    new_user_dict = new_user.model_dump()
    new_user_dict["password"] = crypt.hash(new_user.password)
    new_user_dict["created_date"] = datetime.utcnow()
    new_user_dict["last_login"] = datetime.utcnow()

    insert_new_user = await users_collection.insert_one(new_user_dict)
    if not insert_new_user.inserted_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user")
    return {"detail": f"The user {new_user.username} has been created successfully"}

@router.post("/signin", status_code=status.HTTP_202_ACCEPTED)
async def sign_in_user(username_and_password: OAuth2PasswordRequestForm = Depends()):
    user = await search_user("username", username_and_password.username)
    if not isinstance(user, User):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not crypt.verify(username_and_password.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password Incorrect")

    await delete_existing_token(user)
    token = await get_token(user)
    await users_collection.update_one({"_id": ObjectId(user.id)}, {"$set": {"last_login": datetime.utcnow()}})
    return {"token_type": "Bearer", "token": token}

@router.get("/user/{username}", status_code=status.HTTP_202_ACCEPTED)
@router.get("/user/", status_code=status.HTTP_202_ACCEPTED)
async def get_user(username: str, user: User = Depends(verify_token)):
    search_username = await existing_username(username)
    await id_matching(search_username.id, user.id)
    
    return user_visual_scheme(user.model_dump())
