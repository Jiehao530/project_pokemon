def user_converter(data) -> dict:
    return {
        "id": str(data["_id"]),
        "username": data["username"],
        "password": data["password"],
        "email": data["email"],
        "created_date": data["created_date"],
        "last_login": data["last_login"],
    }

def user_visual_converter(data) -> dict:
    return {
        "id": data["id"],
        "username": data["username"],
        "password": "********",
        "email": data["email"],
        "created_date": data["created_date"],
        "last_login": data["last_login"]
    }

def user_visual_profile_converter(data) -> dict:
    return {
        "username": data["username"],
        "created_date": data["created_date"],
        "last_login": data["last_login"]
    }