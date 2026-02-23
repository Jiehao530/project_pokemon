def shop_config_converter(data) -> dict:
    return {
        "id": data["_id"],
        "refresh_at": data["refresh_at"],
        "last_refresh": data["last_refresh"],
        "refresh_interval_hours": data["refresh_interval_hours"]
    }

def shop_items_pokecoins_pack_converter(data) -> dict:
    return {
        "id": str(data["_id"]),
        "type": data["type"],
        "item_id": data["item_id"],
        "price": float(str(data["price"])),
        "currency": data["currency"]
    }