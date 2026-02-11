from fastapi import APIRouter, status, Depends
from app.schemes.users_scheme import User, UpdateUser
from app.dependencies.auth_depends import get_current_user
from app.services.users_service import UserService

router = APIRouter(tags=["Users"])


@router.get("/user/me", status_code=status.HTTP_202_ACCEPTED)
async def get_user(user: User = Depends(get_current_user)):
    return UserService().get_user(user)

@router.patch("/user/me", status_code=status.HTTP_202_ACCEPTED)
async def update_user(new_data: UpdateUser, user: User = Depends(get_current_user)):
    return await UserService().update_user(new_data, user)

@router.delete("/user/me", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user: User = Depends(get_current_user)):
    return await UserService().delete_user(user)