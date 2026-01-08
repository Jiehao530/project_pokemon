def user_scheme(data) -> dict:
    return {
        "id": str(data["_id"]),
        "username":data["usename"],
        "password":data["password"],
        "email":data["email"],
        "created_date":data["created_date"],
        "last_login":data["last_login"],
    }