def pokemon_figure_converter(data) -> dict:
    return {
        "pokemon_figure_id": str(data["pokemon_figure_id"]),
        "number": data["number"],
        "name": data["name"],
        "type": data["type"],
        "generation": data["generation"],
        "rarity": data["rarity"],
        "points": data["points"]
    }

    