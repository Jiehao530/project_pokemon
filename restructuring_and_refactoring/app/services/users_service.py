from fastapi import HTTPException, status
from app.schemes.users_scheme import User, UpdateUser
from app.utils.users_converters import user_visual_converter
from app.utils.security import crypt_password
from app.db.repositories.users_repository import UserRepository
from app.db.repositories.auth_repository import AuthRepository
from bson.objectid import ObjectId

class UserService:

    def get_user(self, user: User):
        return user_visual_converter(user.model_dump())

    async def update_user(self, new_data: UpdateUser, user: User):
        new_data_dict = new_data.model_dump(exclude_unset=True)
        if new_data.email:
            search_email = await UserRepository.search_user_by_email(new_data.email, user.id)
            if search_email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email is already in use")
        if new_data.username:
            search_username = await UserRepository.search_user_by_username(new_data.username, user.id)
            if search_username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is already in use")
        if new_data.password:
            new_data_dict["password"] = crypt_password(new_data.password)
        
        update = await UserRepository.update_user(user.id, new_data_dict)
        if update == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update Error")
        await AuthRepository.delete_token("user_id", user.id)
        return {"detail": "The user has been update successfully"}

    async def delete_user(self, user: User):
        delete = await UserRepository.delete_user(user.id)
        if delete == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete Error")
        await AuthRepository.delete_token("user_id", ObjectId(user.id))
        return {"detail": f"The user {user.username} has been deleted successfully"}
    
    async def get_user_id(self, username: str):
        user_id = UserRepository.search_user_id_by_username(username)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user_id