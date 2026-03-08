from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from app.utils.security import SECRET, ALGORITHM
from app.db.repositories.users_repository import UserRepository
from app.db.repositories.auth_repository import AuthRepository

async def get_current_user_for_ws(token: str):
    try:
        data_token = jwt.decode(token, SECRET, ALGORITHM)
    except ExpiredSignatureError:
        return None
    except JWTError:
        return None
    
    token_in_database = await AuthRepository.search_token("token", token)
    if not token_in_database:
        return None
        
    username = data_token.get("sub")
    user = await UserRepository.search_user("username", username)
    if user is None:
        return None
    return user