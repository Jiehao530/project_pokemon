from app.enums.shop_type_enum import ShopType
from app.services.pokemon_figure_service import PokemonFigureService
from app.services.pokecoins_service import PokecoinsService

PURCHASING_FUNCTION = {
    ShopType.POKEMON_FIGURE.value: PokemonFigureService.buy_pokemon_figure,
    ShopType.POKECOINS.value: PokecoinsService.buy_pokecoins_pack
}