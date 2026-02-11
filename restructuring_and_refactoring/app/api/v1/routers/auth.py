from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemes.auth_scheme import NewUser
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up_user(new_user: NewUser):
    return await AuthService().signup_user(new_user)

@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login_user(username_password: OAuth2PasswordRequestForm = Depends()):
    return await AuthService().login_user(username_password)