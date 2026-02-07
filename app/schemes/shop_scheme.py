import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from schemes.pokemon_scheme import pokemon_figure_for_sale_scheme

def shop_items_pokecoins_scheme(data) -> dict:
    return {
        "id": str(data["_id"]),
        "type": data["type"],
        "item_id": data["item_id"],
        "price": float(str(data["price"])),
        "currency": data["currency"]
        }

def shop_items_pokemon_figure_scheme(data) -> dict:
    return {
        "id": str(data["_id"]),
        "type": data["type"],
        "pokemon_figure": pokemon_figure_for_sale_scheme(data["pokemon_figure"]),
        "price": data["price"],
        "currency": data["currency"],
        "expires_at": data["expires_at"]
    }