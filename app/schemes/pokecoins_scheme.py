def pokecoins_pack_scheme(data) -> dict:
    return {
        "id": data["_id"],
        "amount": data["amount"],
        "price": float(str(data["price"])),
        "currency": data["currency"]
    }


def pokecoins_scheme(data) -> dict:
    return {
        "user_id": str(data["user_id"]),
        "pokecoins": data["pokecoins"]
    }