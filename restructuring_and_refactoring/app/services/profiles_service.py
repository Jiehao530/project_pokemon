from fastapi import HTTPException, status
from app.db.repositories.users_repository import UserRepository
from app.services.follow_service import FollowService
from app.utils.id_converter import id_converter


class ProfileService:

    async def get_profile(self, user_id: str):
        objectid_user_id = id_converter(user_id)
        profile = await UserRepository.search_user_visual_profile_by_id(objectid_user_id)
        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        
        followers = await FollowService().get_followers_numbers(objectid_user_id)
        following = await FollowService().get_following_numbers(objectid_user_id)
        
        return {
            "profile": profile, 
            "followers": {"number_of_followers": followers}, 
            "following": {"number_of_following": following}
            }