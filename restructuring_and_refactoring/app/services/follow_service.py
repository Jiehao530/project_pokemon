from fastapi import HTTPException, status
from app.db.repositories.follow_repository import FollowRepository
from app.db.repositories.users_repository import UserRepository
from app.schemes.follow_scheme import Follow
from app.schemes.users_scheme import User
from app.utils.id_converter import id_converter
from bson.objectid import ObjectId

class FollowService:

    async def follow_user(self, followed_id: str, user: User):
        objectid_followed_id = id_converter(followed_id)
        search = await FollowRepository.search_existing_follow("follower_id", ObjectId(user.id), "followed_id", objectid_followed_id)
        if isinstance(search, Follow):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already following this user")
            
        follow_data = {
        "follower_id": ObjectId(user.id),
        "followed_id": objectid_followed_id
        }

        insert = await FollowRepository.insert_follow(follow_data)
        if not insert:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Follow Error")
        return {"detail": f"Followed"}

    async def unfollow_user(self, unfollow_id: str, user: User):
        objectid_unfollow_id = id_converter(unfollow_id)
        search = await FollowRepository.search_existing_follow("follower_id", ObjectId(user.id), "followed_id", objectid_unfollow_id)
        if search is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You aren't following this user")
        
        unfollow = await FollowRepository.delete_follow("follower_id", ObjectId(user.id), "followed_id", objectid_unfollow_id)
        if unfollow == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unfollow Error")
        return {"detail": f"Unfollowed"}

    async def get_followers(self, user_id: str):
        objectid_user_id = id_converter(user_id)
        search = await FollowRepository.search_follow("followed_id", objectid_user_id)
        if search is None:
            return {"followers": []}
        followers_id_list = [ObjectId(follow.follower_id) for follow in search]
        search_usernames = await UserRepository.search_username_list_by_id(followers_id_list)
        return {"followers": search_usernames}

    async def get_following(self, user_id: str):
        objectid_user_id = id_converter(user_id)
        search = await FollowRepository.search_follow("follower_id", objectid_user_id)
        if search is None:
            return {"following": []}
        following_id_list = [ObjectId(follow.followed_id) for follow in search]
        search_usernames = await UserRepository.search_username_list_by_id(following_id_list)
        return {"following": search_usernames}

    async def get_followers_numbers(self, user_id):
        search_followers = await FollowRepository.search_follow("followed_id", user_id)
        if search_followers is None:
            return 0
        return len(search_followers)
    
    async def get_following_numbers(self, user_id):
        search_following = await FollowRepository.search_follow("follower_id", user_id)
        if search_following is None:
            return 0
        return len(search_following)
    