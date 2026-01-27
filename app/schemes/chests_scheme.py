def chest_scheme(data) -> dict:
    return {
        "name": data["name"],
        "generation": data["generation"]
    }

def chest_status_scheme(data) -> dict:
    return {
        "chest": data["chest"],
        "last_generated": data["last_generated"],
        "next_chest": data["next_chest"]
    }