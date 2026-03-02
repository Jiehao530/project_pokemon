def pokecoins_converter(data) -> dict:
    return {
        "user_id": str(data["user_id"]),
        "amount": data["amount"],
        "currency": data["currency"]
    }

def pokecoins_pack_converter(data) -> dict:
    return {
        "id": data["_id"],
        "amount": data["amount"],
        "price": data["price"],
        "currency": data["currency"]
    }