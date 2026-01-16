def pokemon_scheme(data) -> dict:
    return {
        "number": data["number"],
        "name": data["name"],
        "type": data["type"],
        "generation": data["generation"]
    }