import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import timedelta

load_dotenv()

SECRET = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM")

CRYPT_CONTEXT = CryptContext(schemes=["bcrypt"])

TOKEN_DURATION = timedelta(days=1)

