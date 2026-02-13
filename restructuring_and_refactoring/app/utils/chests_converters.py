def chest_scheme(data) -> dict:
    return {
        "id": data["_id"],
        "name": data["name"],
        "generation": data["generation"]
    }