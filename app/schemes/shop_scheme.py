import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from schemes.pokemon_scheme import pokemon_figure_for_sale_scheme

def shop_status_scheme(data) -> dict:
    return {
        "id": str(data["_id"]),
        "last_generated": data["last_generated"],
        "next_shop": data["next_shop"]
    }

def shop_pokemon_figures_scheme(data) -> list:
    pokemon_figures_list = []
    for data_pokemon_figure_shop in data:
        pokemon_figure = {
            "pokemon_figure_id": str(data_pokemon_figure_shop["_id"]),
            "pokemon_figure": pokemon_figure_for_sale_scheme(data_pokemon_figure_shop["pokemon_figure"])
        }
        pokemon_figures_list.append(pokemon_figure)
    return pokemon_figures_list