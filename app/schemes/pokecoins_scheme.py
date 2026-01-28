def pokecoins_scheme(data) -> dict:
    return {
        "user_id": str(data["user_id"]),
        "pokecoins": data["pokecoins"]
    }