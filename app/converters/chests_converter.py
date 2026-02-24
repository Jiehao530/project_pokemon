def chest_converter(data) -> dict:
    return {
        "id": data["_id"],
        "name": data["name"],
        "generation": data["generation"]
    }

def chest_status_database_converter(data) -> dict:
    return {
        "id": str(data["_id"]),
        "user_id": str(data["user_id"]),
        "chest": data["chest"],
        "last_generated": data["last_generated"],
        "next_chest": data["next_chest"]
    }
def chest_status_converter(data) -> dict:
    return {
        "chest": data["chest"],
        "last_generated": data["last_generated"],
        "next_chest": data["next_chest"]
    }