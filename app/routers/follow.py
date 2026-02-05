import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException, Depends
from helpers.follow_helper import verify_follow, search_follow
from helpers.users_helper import verify_token, verify_user_id
from models.follow_model import Follow
from models.users_model import User
from services.database import follow_collection, profile_collection
from bson import ObjectId

router = APIRouter(tags=["follow"])

#Endpoint para seguir a un usuario
@router.post("/profile/{followed_id}/follow", status_code=status.HTTP_202_ACCEPTED)
async def follow_user(followed_id: str, user: User = Depends(verify_token)):
    """
    Seguir usuario
    --------------------------------------------------------------
    Flujo:
    1. Convierte el followed_id en un ObjectID
    2. Busca si ya estaba siguiendo el usuario
    3. Inserta los datos
    4. Retorna que lo ha seguido

    Respuestas:
    - 202: Se ha seguido
    - 400: Ya lo estaba siguiendo
    - 400: Error al seguir
    - Otros: Consultar las funciones verify_user_id y verify_token en users_helpers
    """
    #Al convertir en ObjectID se puede saber si es válido o inválido
    objectid_followed_id = verify_user_id(followed_id)
    #Al buscar si lo estaba siguiendo, hay que buscar el documento que contengan estas coincidencias
    search = await verify_follow("follower_id", ObjectId(user.id), "followed_id", objectid_followed_id)
    if isinstance(search, Follow):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already following this user")
    
    follow_data = {
        "follower_id": ObjectId(user.id),
        "followed_id": objectid_followed_id
    }
    insert_follow_data = await follow_collection.insert_one(follow_data)
    #Manteja error si el documento no es correcto
    if not insert_follow_data.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Follow Error")
    return {"detail": f"Followed"}

#Endpoint para dejar de seguir a un usuario
@router.delete("/profile/{unfollow_id}/unfollow", status_code=status.HTTP_202_ACCEPTED)
async def unfollow_user(unfollow_id: str, user: User = Depends(verify_token)):
    """
    Dejar de seguir
    ----------------------------------
    Flujo:
    1. Convierte el unfollow_id en un ObjectID
    2. Busca si no estaba siguiendo el usuario
    3. Elimina el documento
    4. Retorna que lo ha dejado de seguir

    Respuestas:
    - 202: Se ha dejado de seguir
    - 400: No lo estaba siguiendo
    - 400: Error al dejar de seguir
    - Otros: Consultar las funciones verify_user_id y verify_token en users_helpers
    """
    objectid_unfollow_id = verify_user_id(unfollow_id)
    #Hay que verificar si no lo estaba siguiendo para controlar el error
    search = await verify_follow("follower_id", ObjectId(user.id), "followed_id", objectid_unfollow_id)
    if search is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You aren't following this user")

    unfollow = await follow_collection.delete_one({"follower_id": ObjectId(user.id), "followed_id": objectid_unfollow_id})
    if unfollow.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unfollow Error")
    return {"detail": f"Unfollowed"}

#Endpoint para obtener lista de seguidores
@router.get("/profile/{user_id}/followers", status_code=status.HTTP_202_ACCEPTED)
async def get_followers(user_id: str):
    """
    Obtener seguidores
    ----------------------------------
    Flujo:
    1. Convierte el user_id en un ObjectID
    2. Busca los seguidores
    3. Obtiene los seguidores

    Respuestas:
    - 202: Se ha obtenido los seguidores
    - Otros: Consultar la función verify_user_id
    """
    objectid_user_id = verify_user_id(user_id)
    search = await search_follow("followed_id", objectid_user_id)
    #Si no hay seguidores hay que retornar una lista vacía
    if search is None:
        return {"followers": []}
    #Hay que hacer una nueva lista que contenga solo los ID de los seguidores y convertirlos en ObjectID para luego poder buscarlos
    followers_id_list = [ObjectId(follower_id["follower_id"]) for follower_id in search]
    followers_profiles = await profile_collection.find({"user_id": {"$in": followers_id_list}}).to_list(1000)
    #Hacer una nueva lista con solo los nombres de usuario de los seguidores
    followers = [follower_username["username"] for follower_username in followers_profiles]
    return {"followers": followers}

#Endpoint para obtener lista de siguiendo
@router.get("/profile/{user_id}/following", status_code=status.HTTP_202_ACCEPTED)
async def get_following(user_id: str):
    """
    Obtener siguiendo
    ----------------------------------
    Flujo:
    1. Convierte el user_id en un ObjectID
    2. Busca los usuarios que sigue
    3. Obtiene los usuarios que sigue

    Respuestas:
    - 202: Se ha obtenido los seguidores
    - Otros: Consultar la función verify_user_id
    """
    objectid_user_id = verify_user_id(user_id)
    search = await search_follow("follower_id", objectid_user_id)
    #Si no sigue a nadie hay que retornar una lista vacía
    if search is None:
        return {"following": []}
    #Hay que hacer una nueva lista que contenga solo los IDs de usuario que sigue y convertirlos en ObjectID para luego poder buscarlos
    following_id_list = [ObjectId(followed_id["followed_id"]) for followed_id in search]
    following_profiles = await profile_collection.find({"user_id": {"$in": following_id_list}}).to_list(1000)
    #Hacer una nueva lista con solo los nombres de usuario que sigue
    following = [following_username["username"] for following_username in following_profiles]
    return {"following": following}