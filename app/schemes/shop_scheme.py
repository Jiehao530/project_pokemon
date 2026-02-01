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

def shop_pokemon_figures_scheme(data) -> dict:
    return {
        "shop_id": str(data["shop_id"]),
        "shop_name": data["shop_name"],
        "pokemon_figures": [pokemon_figure_for_sale_scheme(pokemon_figure) for pokemon_figure in data["pokemon_figures"]]
    }