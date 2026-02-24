def pokecoins_converter(data) -> dict:
    return {
        "user_id": str(data["user_id"]),
        "amount": data["amount"],
        "currency": data["currency"]
    }