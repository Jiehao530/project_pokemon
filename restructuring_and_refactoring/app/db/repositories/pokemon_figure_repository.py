from app.db.repositories.collections import pokemon_figure_collection

class PokemonFigureRepository:

    @staticmethod
    async def insert_pokemon_figure(data_pokemon_figure: dict):
        insert = await pokemon_figure_collection.insert_one(data_pokemon_figure)
        return insert.acknowledged