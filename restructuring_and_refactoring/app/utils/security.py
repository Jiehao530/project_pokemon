from app.constants.auth_constants import CRYPT_CONTEXT, SECRET, ALGORITHM
from jose import jwt

def crypt_password(password: str):
    return CRYPT_CONTEXT.hash(password)

def verify_password(password: str, userdb_password: str):
    return CRYPT_CONTEXT.verify(password, userdb_password)

def encode_token(data_token: dict):
    return jwt.encode(data_token, SECRET, ALGORITHM)
