from fastapi import FastAPI
from routers import users, follow, profiles, chests, pokemon, pokecoins, shop
app = FastAPI()

app.include_router(users.router)
app.include_router(follow.router)
app.include_router(profiles.router)
app.include_router(chests.router)
app.include_router(pokemon.router)
app.include_router(pokecoins.router)
app.include_router(shop.router)