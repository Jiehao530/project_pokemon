import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.users_model import NewUser, User, UpdateUser
from schemes.users_scheme import user_visual_scheme
from helpers.users_helper import search_user, delete_existing_token, get_token, verify_token, insert_other_data
from datetime import datetime
from services.database import users_collection, token_collection
from passlib.context import CryptContext
from bson import ObjectId

router = APIRouter(tags=["Users"])
crypt = CryptContext(schemes=["bcrypt"])

#Sign Up User source code
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
    await insert_other_data(insert_new_user.inserted_id, new_user.username, new_user_dict["created_date"])
    return {"detail": f"The user {new_user.username} has been created successfully"}

#Sign In User source code
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

#Get User source code
@router.get("/user/me", status_code=status.HTTP_202_ACCEPTED)
async def get_user(user: User = Depends(verify_token)):
    return user_visual_scheme(user.model_dump())

#Update User source code
@router.patch("/user/me", status_code=status.HTTP_202_ACCEPTED)
async def update_user(new_data: UpdateUser, user: User = Depends(verify_token)):
    new_data_dict = new_data.model_dump(exclude_unset=True)
    if new_data.email:
        search_email = await users_collection.find_one({"email": new_data.email, "_id": {"$ne": ObjectId(user.id)}})
        if isinstance(search_email, User):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email is already in use")
    if new_data.username:
        search_username = await users_collection.find_one({"username": new_data.username, "_id": {"$ne": ObjectId(user.id)}})
        if isinstance(search_username, User):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is already in use")
    if new_data.password:
        hash_password = crypt.hash(new_data.password)
        new_data_dict["password"] = hash_password

    update = await users_collection.update_one({"_id": ObjectId(user.id)}, {"$set": new_data_dict})
    if update.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update Error")
    return {"detail": "The user has been update successfully"}

#Delete User source code
@router.delete("/user/me", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user: User = Depends(verify_token)):
    delete = await users_collection.delete_one({"_id": ObjectId(user.id)})
    if delete.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete Error")
    await token_collection.delete_one({"_id": ObjectId(user.id)})
    return {"detail": f"The user {user.username} has been deleted successfully"}

#Log Out User source code
@router.post("/logout", status_code=status.HTTP_202_ACCEPTED)
async def log_out_user(user: User = Depends(verify_token)):
    delete_token = await token_collection.delete_one({"user_id": ObjectId(user.id)})
    if delete_token.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Log Out Error")
    return {"detail": f"You have been successfully logged out"}