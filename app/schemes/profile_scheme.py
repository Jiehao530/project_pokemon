def profile_scheme(data) -> dict:
    return {
        "user_id": str(data["user_id"]),
        "username": data["username"],
        "created_date": data["created_date"]
    }