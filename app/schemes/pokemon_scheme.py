def pokemon_scheme(data) -> dict:
    return {
        "number": data["number"],
        "name": data["name"],
        "type": data["type"],
        "generation": data["generation"]
    }

def pokemon_figures_scheme(data) -> dict:
    return {
        "pokemon_figure": data["pokemon_figure"]
    }