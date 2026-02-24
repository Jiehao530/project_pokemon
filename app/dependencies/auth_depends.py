from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from app.utils.security import SECRET, ALGORITHM
from app.db.repositories.users_repository import UserRepository
from app.db.repositories.auth_repository import AuthRepository

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2)):
    try:
        data_token = jwt.decode(token, SECRET, ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is invalid")
    
    token_in_database = await AuthRepository.search_token("token", token)
    if not token_in_database:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is invalid")
    username = data_token.get("sub")
    user = await UserRepository.search_user("username", username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user