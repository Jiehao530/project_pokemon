from enum import Enum

class Currency(str, Enum):
    POKECOINS = "pokecoins"
    REAL_MONEY = "real_money"