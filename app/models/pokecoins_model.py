from pydantic import BaseModel

class PokeCoins(BaseModel):
    user_id: str
    pokecoins: int