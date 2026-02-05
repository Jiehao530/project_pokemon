import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.database import profile_collection
from models.profile_model import Profile
from schemes.profile_scheme import profile_scheme

#Función para obtener los datos del perfil
async def search_profile(field: str, value):
    profile = await profile_collection.find_one({field: value})
    if not profile:
        return None
    return Profile(**profile_scheme(profile))
