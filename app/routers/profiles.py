import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import APIRouter, status, HTTPException
from helpers.users_helper import verify_user_id
from helpers.profiles_helper import search_profile
from helpers.follow_helper import get_followers_numbers, get_following_numbers
from schemes.profile_scheme import profile_visual_scheme

router = APIRouter(tags=["Profiles"])

#Endpoint para obtener el perfil del usuario
@router.get("/profile/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_profile(user_id: str):
    """
    Obtener perfil
    ---------------------------------------------------------------
    Flujo:
    1. Obtiene el ID de usuario
    2. Busca el perfil del usuario
    3. Obtiene los números de seguidores que tiene el usuario
    4. Obtiene los números de siguiendo que tiene el usuario
    5. Retorna un json compuesto

    Respuestas:
    - 202: Se ha obtenido el perfil del usuario 
    - Otros: Consultar la función verify_user_id en users_helpers
    """
    #Hay que asegurarse que el ID de usuario sea válido
    objectid_user_id = verify_user_id(user_id)
    profile = await search_profile("user_id", objectid_user_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        
    followers = await get_followers_numbers(profile.user_id)
    following = await get_following_numbers(profile.user_id)
    visual_profile = profile_visual_scheme(profile.model_dump())
    #Retornamos un json compuesto que va a formar los datos del perfil
    return {
        "profile": visual_profile, 
        "followers": {"number_of_followers": followers}, 
        "following": {"number_of_following": following}
        }
    