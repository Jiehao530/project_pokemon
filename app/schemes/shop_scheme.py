def shop_status_scheme(data) -> dict:
    return {
        "id": str(data["_id"]),
        "last_generated": data["last_generated"],
        "next_shop": data["next_shop"]
    }

def shop_pokemon_figures_scheme(data) -> dict:
    return {
        "shop_id": str(data["shop_id"]),
        "shop_name": data["shop_name"],
        "pokemon_figures": data["pokemon_figures"]
    }