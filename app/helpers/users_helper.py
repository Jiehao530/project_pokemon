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

#Función para buscar el usuario
async def search_user(field: str, value):
    """
    Flujo:
    1. Busca el documento en la colección de usuarios mediante field y value
    2. Retorna respuestas según el resultado de la búsqueda

    Respuestas:
    - Return User
    - Return None
    """
    user = await users_collection.find_one({field: value})
    if user:
        #Necesitamos usar un scheme porque el ID que hay en la base lo guarda como ObjectID
        #Si no se utiliza da un error
        return User(**user_scheme(user))
    else:
        return None

#Función para eliminar token
async def delete_existing_token(data_user: User):
    """
    Flujo:
    1. Elimina el token mediante el ID del usuario
    
    Respuestas:
    - None
    """
    #Al eliminarlo podemos eliminar tanto las caducadas como las no caducadas para garantizar seguridad
    search_token = await token_collection.delete_one({"user_id": ObjectId(data_user.id)})
    if search_token.deleted_count == 0:
        pass

#Función para generar token de sesión JWT
async def get_token(data_user: User):
    data_token = {
        "sub": data_user.username,
        "exp": datetime.utcnow() + TOKEN_DURATION
    }
    #Codificamos el token con SECRET y ALGORITHM para garantizar su integridad y seguridad
    token = jwt.encode(data_token, SECRET, ALGORITHM)
    #Guardamos el token en la base de datos para poder invalidarlo al cerrar sesión incluso si aún no ha expirado
    await token_collection.insert_one({
        "user_id": ObjectId(data_user.id),
        "username": data_user.username,
        "token": token,
        "created_at": datetime.utcnow()
    })
    return token

#Función para verificar el token de sesión 
async def verify_token(token: str = Depends(OAuth2)):
    """
    Flujo:
    1. Decodea el token de sesión
    2. Busca si el token de sesión esta en la base de datos
    3. Obtenemos del token el username
    4. Busca el usuario 
    5. Retorna el usuario

    Respuestas:
    - 401: El token de sesión ha expirado
    - 401: El token de sesión es inválido
    - 401: El token de sesión es inválido porque no esta en la base de datos
    - Return user
    """
    #Manejo de errores para validar caducidad y para descartar tokens maliciosos
    try:
        data_token = jwt.decode(token, SECRET, ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is invalid")
    
    #Hay que asegurarse que el token este en la base de datos para evitar tokens válidos sin caducar sean inválidos
    token_in_database = await token_collection.find_one({"token": token})
    if not token_in_database:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is invalid")
    username = data_token.get("sub")
    user = await search_user("username", username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

async def insert_other_data(user_id: str, username: str, created_date: datetime):
    await profile_collection.insert_one({
        "user_id": ObjectId(user_id),
        "username": username,
        "created_date": created_date
    })

#Función para convertir en ObjectID
def verify_user_id(user_id: str):
    try:
         return ObjectId(user_id) 
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id")