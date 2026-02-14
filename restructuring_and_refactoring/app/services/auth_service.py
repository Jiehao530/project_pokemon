from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.repositories.auth_repository import AuthRepository
from app.db.repositories.users_repository import UserRepository
from app.schemes.auth_scheme import NewUser
from app.schemes.users_scheme import User
from app.utils.id_converter import id_converter
from app.utils.security import crypt_password, verify_password, encode_token
from datetime import datetime, timedelta

TOKEN_DURATION = timedelta(days=1)

class AuthService:

    async def get_token(self, data_user: User):
        data_token = {
            "sub": data_user.username,
            "exp": datetime.utcnow() + TOKEN_DURATION
            }
        
        token = encode_token(data_token)
        data = {
            "user_id": id_converter(data_user.id),
            "username": data_user.username,
            "token": token,
            "created_at": datetime.utcnow()
            }
        await AuthRepository.insert_token(data)
        return token

    async def signup_user(self, new_user: NewUser):
        search_email = await UserRepository.search_user("email", new_user.email)
        if isinstance(search_email, User):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email is already in use")
        search_username = await UserRepository.search_user("username", new_user.username)
        if isinstance(search_username, User):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is already in use")
        
        new_user_dict = new_user.model_dump()
        new_user_dict["password"] = crypt_password(new_user.password)
        new_user_dict["created_date"] = datetime.utcnow()
        new_user_dict["last_login"] = datetime.utcnow()

        insert_new_user = await UserRepository.insert_new_user(new_user_dict)
        if not insert_new_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user")
        return {"detail": f"The user {new_user.username} has been created successfully"}
    
    async def login_user(self, username_password: OAuth2PasswordRequestForm):
        user = await UserRepository.search_user("username", username_password.username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
        if not verify_password(username_password.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password Incorrect")
        
        objectid_user_id = id_converter(user.id)
        await AuthRepository.delete_token("user_id", objectid_user_id)
        token = self.get_token(user)
        await UserRepository.update_last_login(objectid_user_id)

        return {"token_type": "Bearer", "access_token": token}

    async def logout_user(self, user: User):
        delete_token = await AuthRepository.delete_token("user_id", id_converter(user.id))
        if delete_token == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Log Out Error")
        return {"detail": f"You have been successfully logged out"}

