from fastapi import HTTPException, status
from app.db.repositories.pokemon_figure_repository import PokemonFigureRepository
from app.db.repositories.shop_repository import ShopRepository
from app.managers.pokemon_figure_manager import PokemonFigureManager
from app.schemes.pokemon_figure_scheme import PokemonFigure
from app.converters.pokemon_figure_converter import pokemon_figure_converter
from app.utils.id_converter import id_converter
from app.constants.price_constants import PRICE_RARITY, PRICE_POINTS
from app.enums.shop_type_enum import ShopType
from app.enums.currency_enum import Currency
from datetime import datetime, timedelta

class PokemonFigureService:

    async def get_your_pokemon_figures(self, user_id: str, number, name, type, generation, rarity, points, page, pagesize):
        objectid_user_id = id_converter(user_id)

        search_parameters = {"user_id": objectid_user_id}

        if number is not None:
            search_parameters["pokemon_figure.number"] = number
        if name is not None:
            search_parameters["pokemon_figure.type"] = name
        if type is not None:
            search_parameters["pokemon_figure.type"] = {"$in": type}
        if generation is not None:
            search_parameters["pokemon_figure.generation"] = generation
        if rarity is not None:
            search_parameters["pokemon_figure.rarity"] = rarity
        if points is not None:
            search_parameters["pokemon_figure.points"] = points

        total_figures = await PokemonFigureRepository.count_documents(search_parameters)
        pokemon_figures_list = await PokemonFigureRepository.search_pokemon_figures(search_parameters, page, pagesize)
        pokemon_figures = [PokemonFigure(**pokemon_figure_converter(pokemon_figure)) for pokemon_figure in pokemon_figures_list]
        
        return {
            "pokemon_figures": pokemon_figures,
            "page": page,
            "pagesize": pagesize,
            "total": total_figures,
            "total_pages": (total_figures + pagesize - 1) // pagesize
            }
    
    async def new_pokemon_figures_for_shop(self, expire_time: datetime):
        pokemon_figures_list = await PokemonFigureManager.get_pokemon_figures_for_shop(3)
        
        document_list = []
        for pokemon_figure in pokemon_figures_list:
            data_pokemon_figure = {
                "type": ShopType.POKEMON_FIGURE.value,
                "pokemon_figure": pokemon_figure,
                "price": PRICE_RARITY[pokemon_figure["rarity"]] + PRICE_POINTS[pokemon_figure["points"]],
                "currency": Currency.POKECOINS.value,
                "expires_at": expire_time
            }
            document_list.append(data_pokemon_figure)

        insert = await ShopRepository.insert_many_in_shop_items(document_list)
        if not insert:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insert Pokémon Figure For Shop Error")
        return True       