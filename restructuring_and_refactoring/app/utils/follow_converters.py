def follow_converter(data) -> dict:
    return {
        "follower_id": str(data["follower_id"]),
        "followed_id": str(data["followed_id"])
    }