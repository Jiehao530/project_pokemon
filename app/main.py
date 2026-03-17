from fastapi import FastAPI
from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.users import router as users_router
from app.api.v1.routers.follow import router as follow_router
from app.api.v1.routers.profiles import router as profile_router
from app.api.v1.routers.chests import router as chests_router
from app.api.v1.routers.pokemon_figures import router as pokemon_figures_router
from app.api.v1.routers.pokecoins import router as pokecoins_router
from app.api.v1.routers.shop import router as shop_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(follow_router)
app.include_router(profile_router)
app.include_router(chests_router)
app.include_router(pokemon_figures_router)
app.include_router(pokecoins_router)
app.include_router(shop_router)
