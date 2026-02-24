from app.converters.pokemon_figure_converter import pokemon_figure_for_shop_converter

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

def shop_items_pokemon_figure_converter(data) -> dict:
    return {
        "id": str(data["_id"]),
        "type": data["type"],
        "pokemon_figure": pokemon_figure_for_shop_converter(data["pokemon_figure"]),
        "price": data["price"],
        "currency": data["currency"],
        "expires_at": data["expires_at"],
    }