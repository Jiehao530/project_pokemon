def pokemon_scheme(data) -> dict:
    return {
        "number": data["number"],
        "name": data["name"],
        "type": data["type"],
        "generation": data["generation"]
    }

def pokemon_figure_scheme(data) -> dict:
    return {
        "pokemon_figure_id": str(data["pokemon_figure_id"]),
        "number": data["number"],
        "name": data["name"],
        "type": data["type"],
        "generation": data["generation"],
        "rarity": data["rarity"],
        "points": data["points"],
    }

def pokemon_figures_scheme(data) -> dict:
    return {
        "pokemon_figure": pokemon_figure_scheme(data["pokemon_figure"])
    }

def pokemon_figure_for_sale_scheme(data) -> dict:
    return {
        "number": data["number"],
        "name": data["name"],
        "type": data["type"],
        "generation": data["generation"],
        "rarity": data["rarity"],
        "points": data["points"],
        "price": data["price"]
    }