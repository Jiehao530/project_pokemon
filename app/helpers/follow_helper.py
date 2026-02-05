import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.database import follow_collection
from models.follow_model import Follow
from schemes.follow_scheme import follow_scheme
from bson import ObjectId

#Función para obtener el documento de seguir (2 parámetros)
async def verify_follow(field: str, value, field_2: str, value_2):
    """
    Obtener seguir
    ---------------------------------
    Flujo:
    1. Busca el documento de seguir
    2. Retorna el documento

    Respuestas:
    - Retorna None
    - Retorna Follow
    """
    verify = await follow_collection.find_one({field: value, field_2: value_2})
    if not verify:
        return None
    return Follow(**follow_scheme(verify))

#Función para obtener la lista de documentos de seguir
async def search_follow(field: str, value):
    """
    Obtener lista de documentos
    ---------------------------------
    Flujo:
    1. Busca todos los documentos de seguir que coincidan con los parámetros
    2. Retorna la lista de documentos

    Respuestas:
    - Retorna None
    - Retorna una lista
    """
    follow = await follow_collection.find({field: value}).to_list(1000)
    if not follow:
        return None
    return [follow_scheme(data) for data in follow]

#Función para obtener el número de seguidores
async def get_followers_numbers(user_id: str):
    """
    Obtener número de seguidores
    ---------------------------------
    Flujo:
    1. Busca todos los documentos de seguir
    2. Retorna la cantidad de documentos que ha encontrado

    Respuestas:
    - Retorna 0
    - Retorna followers_numbers
    """
    search = await search_follow("followed_id", ObjectId(user_id))
    #Si no hay documentos quiere decir que no hay seguidores por eso 0
    if search is None:
        return 0
    followers_numbers = len(search)
    return followers_numbers

#Función para obtener el número de siguiendo
async def get_following_numbers(user_id: str):
    """
    Obtener número de siguiendo
    ---------------------------------
    Flujo:
    1. Busca todos los documentos de siguiendo
    2. Retorna la cantidad de documentos que ha encontrado

    Respuestas:
    - Retorna 0
    - Retorna following_numbers
    """
    search = await search_follow("follower_id", ObjectId(user_id))
    #Si no hay documentos quiere decir que no sigue a nadie por eso 0
    if search is None:
        return 0
    following_numbers = len(search)
    return following_numbers