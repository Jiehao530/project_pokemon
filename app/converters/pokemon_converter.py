def pokemon_converter(data) -> dict:
    return {
        "id": data["_id"],
        "number": data["number"],
        "name": data["name"],
        "type": data["type"],
        "generation": data["generation"]
    }