from pydantic import BaseModel

class Follow(BaseModel):
    follower_id: str
    followed_id: str