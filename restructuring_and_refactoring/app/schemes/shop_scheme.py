from pydantic import BaseModel
from datetime import datetime
from app.enums.shop_type_enum import ShopType
from app.enums.currency_enum import Currency
from app.schemes.pokemon_figure_scheme import PokemonFigureShop

class ShopConfig(BaseModel):
    id: str
    refresh_at: datetime
    last_refresh: datetime
    refresh_interval_hours: int

class ShopPokecoinsPack(BaseModel):
    id: str
    type: ShopType
    item_id: str
    price: float
    currency: Currency

class ShopItemPokemonFigure(BaseModel):
    id: str
    type: ShopType
    pokemon_figure: PokemonFigureShop
    price: int
    currency: Currency
    expires_at: datetime