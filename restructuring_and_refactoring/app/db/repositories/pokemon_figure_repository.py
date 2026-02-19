from app.db.repositories.collections import pokemon_figure_collection

class PokemonFigureRepository:

    @staticmethod
    async def insert_pokemon_figure(data_pokemon_figure: dict):
        insert = await pokemon_figure_collection.insert_one(data_pokemon_figure)
        return insert.acknowledged

    @staticmethod
    async def count_documents(search_parameters: dict):
        count = await pokemon_figure_collection.count_documents(search_parameters)
        return count

    @staticmethod
    async def search_pokemon_figures(search_parameters: dict, page: int, pagesize: int):
        skip = (page - 1) * pagesize
        pokemon_figures_list = await pokemon_figure_collection.find(search_parameters).skip(skip).limit(pagesize).to_list()
        return pokemon_figures_list