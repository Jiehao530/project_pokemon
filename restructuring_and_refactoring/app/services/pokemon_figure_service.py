from app.db.repositories.pokemon_figure_repository import PokemonFigureRepository
from app.converters.pokemon_figure_converter import pokemon_figure_converter
from app.utils.id_converter import id_converter

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
        pokemon_figures = [pokemon_figure_converter(pokemon_figure) for pokemon_figure in pokemon_figures_list]
        
        return {
            "pokemon_figures": pokemon_figures,
            "page": page,
            "pagesize": pagesize,
            "total": total_figures,
            "total_pages": (total_figures + pagesize - 1) // pagesize
            }