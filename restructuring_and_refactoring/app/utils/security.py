import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt

load_dotenv()

crypt = CryptContext(schemes=["bcrypt"])
SECRET = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM")

def crypt_password(password: str):
    return crypt.hash(password)

def verify_password(password: str, userdb_password: str):
    return crypt.verify(password, userdb_password)

def encode_token(data_token: dict):
    return jwt.encode(data_token, SECRET, ALGORITHM)
