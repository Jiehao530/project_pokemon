from fastapi import FastAPI
from routers import users, follow, profiles
app = FastAPI()

app.include_router(users.router)
app.include_router(follow.router)
app.include_router(profiles.router)