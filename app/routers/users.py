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

#Endpoint para resolver un nombre de usuario y obtener el ID del usuario de la base de datos
@router.get("/resolve/username/{username}", status_code=status.HTTP_202_ACCEPTED)
async def get_user_id(username: str):
    """
    Obtener el ID de usuario
    ------------------------------------------------
    Flujo:
    1. Busca el usuario por username
    2. Retorna solo el ID del usuario

    Respuestas:
    - 202: El ID del usuario ha sido encontrado
    - 404: El ID del usuario no ha sido encontrado
    """
    #Encuentra al usuario que esta en la base de datos
    user = await search_user("username", username)
    #Al no encontrarlo devuelve error
    if user is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    #Devuelve solo el ID del usuario para no exponer todo el documento
    return {"user_id": user.id}

#Endpoint para crear un nuevo usuario
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up_user(new_user: NewUser):
    """
    Registrar un nuevo usuario 
    -------------------------------------------------------------------------------
    Flujo:
    1. Verifica que el correo y el nombre de usuario no estén en uso
    2. Hashea la contraseña para almacenarla en la base de datos de forma segura
    3. Añade nuevos elementos al documento 
    4. Inserta el documento en la base de datos
    5. Retorna mensaje de creación exitosa

    Respuestas:
    - 201: El usuario creado
    - 400: Correo o nombre de usuario usados
    - 400: Error al crear el usuario
    """
    #Controla el nombre de usuario y correo para evitar duplicados 
    search_email = await search_user("email", new_user.email)
    if isinstance(search_email, User):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email is already in use")
    search_username = await search_user("username", new_user.username)
    if isinstance(search_username, User):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is already in use")
    
    new_user_dict = new_user.model_dump() #Convierte el modelo Pydantic a dict para poder modificarlo antes de insertarlo
    new_user_dict["password"] = crypt.hash(new_user.password) #Hashea la contraseña para no almacenar texto plano
    new_user_dict["created_date"] = datetime.utcnow()
    new_user_dict["last_login"] = datetime.utcnow()

    insert_new_user = await users_collection.insert_one(new_user_dict)
    if not insert_new_user.inserted_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user")
    await insert_other_data(insert_new_user.inserted_id, new_user.username, new_user_dict["created_date"])
    return {"detail": f"The user {new_user.username} has been created successfully"}

#Endpoint para obtener el token de sesión
@router.post("/signin", status_code=status.HTTP_202_ACCEPTED) 
async def sign_in_user(username_and_password: OAuth2PasswordRequestForm = Depends()):
    """
    Iniciar sesión
    ------------------------------
    Flujo:
    1. Busca el usuario
    2. Comprueba la contraseña en claro con la contraseña hasheada
    3. Elimina el token de sesión existente que esta en la base de datos
    4. Obtiene un nuevo token de sesión
    5. Actualiza la última sesión del usuario
    6. Retorna el token de sesión

    Respuestas:
    - 202: Inicio de sesión correcto
    - 404: Usuario no encontrado
    - 401: Contraseña incorrecta
    """
    #Encuentra al usuario y si no lo encuentra lanza error 404
    user = await search_user("username", username_and_password.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
    #Verifica si la contraseña es la misma que esta en la base y si no es la misma lanza error 401 
    if not crypt.verify(username_and_password.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password Incorrect")
    
    #Elimina los token de sesión caducados para hacer limpieza en la base y para mejorar la seguridad
    await delete_existing_token(user)
    token = await get_token(user)
    await users_collection.update_one({"_id": ObjectId(user.id)}, {"$set": {"last_login": datetime.utcnow()}})
    return {"token_type": "Bearer", "token": token}

#Endpoint para obtener los datos del usuario
@router.get("/user/me", status_code=status.HTTP_202_ACCEPTED)
async def get_user(user: User = Depends(verify_token)):
    """
    Obtener usuario
    -----------------------------------------------------------
    Flujo:
    1. Obtiene el usuario a través de la verificación del token
    2. Retorna los datos del usuario
    
    """

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