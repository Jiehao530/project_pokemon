import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from app.schemes.users_scheme import User
from app.db.repositories.auth_repository import AuthRepository
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from jose import jwt

load_dotenv()

crypt = CryptContext(schemes=["bcrypt"])
TOKEN_DURATION = timedelta(days=1)
SECRET = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM")

def crypt_password(password: str):
    return crypt.hash(password)

def verify_password(password: str, userdb_password: str):
    return crypt.verify(password, userdb_password)

async def get_token(data_user: User):
    data_token = {
        "sub": data_user.username,
        "exp": datetime.utcnow() + TOKEN_DURATION
    }

    token = jwt.encode(data_token, SECRET, ALGORITHM)

    data = {
        "user_id": ObjectId(data_user.id),
        "username": data_user.username,
        "token": token,
        "created_at": datetime.utcnow()
    }
    
    await AuthRepository.insert_token(data)

    return token
