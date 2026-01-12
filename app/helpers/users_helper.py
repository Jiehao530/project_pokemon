import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from services.database import users_collection, token_collection, profile_collection
from models.users_model import User
from schemes.users_scheme import user_scheme
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from bson import ObjectId

TOKEN_DURATION = timedelta(days=1)
SECRET = "e3f1a8b7c9d6e4f2a1b0c3d5e7f8a9b6c4d2e0f1a3b5c7d9e6f4a2b0c1d3e5f7"
ALGORITHM = "HS256"
OAuth2 = OAuth2PasswordBearer(tokenUrl="/signin")

async def search_user(field: str, value):
    user = await users_collection.find_one({field: value})
    if user:
        return User(**user_scheme(user))
    else:
        return None

async def delete_existing_token(data_user: User):
    search_token = await token_collection.delete_one({"user_id": ObjectId(data_user.id)})
    if search_token.deleted_count == 0:
        pass

async def get_token(data_user: User):
    data_token = {
        "sub": data_user.username,
        "exp": datetime.utcnow() + TOKEN_DURATION
    }
    token = jwt.encode(data_token, SECRET, ALGORITHM)
    await token_collection.insert_one({
        "user_id": ObjectId(data_user.id),
        "username": data_user.username,
        "token": token,
        "created_at": datetime.utcnow()
    })
    return token
    
async def verify_token(token: str = Depends(OAuth2)):
    try:
        data_token = jwt.decode(token, SECRET, ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is invalid")
    
    token_in_database = await token_collection.find_one({"token": token})
    if not token_in_database:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is invalid")
    username = data_token.get("sub")
    user = await search_user("username", username)
    return user

async def existing_username(username: str):
    user = await search_user("username", username)
    if not isinstance(user, User):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

async def id_matching(username_id, user_id):
    if username_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don’t have permission to access this user")

async def insert_other_data(user_id: str, username: str, created_date: datetime):
    await profile_collection.insert_one({
        "user_id": ObjectId(user_id),
        "username": username,
        "created_date": created_date
    })