def shop_items_pokecoins_scheme(data):
    return {
        "id": str(data["_id"]),
        "type": data["type"],
        "item_id": data["item_id"],
        "price": float(str(data["price"])),
        "currency": data["currency"]
        }
