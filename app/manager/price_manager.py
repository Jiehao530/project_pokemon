import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.pokemon_model import Rarity

class PriceManager:
    PRICE_RARITY = {
        Rarity.COMMON.value: 80,
        Rarity.RARE.value: 120,
        Rarity.EPIC.value: 150,
        Rarity.LEGENDARY.value: 200
    }
    PRICE_POINTS = {
        1: 10,
        2: 20,
        3: 30,
        4: 40,
        5: 50
    }

    def __init__(self, rarity: int, points: int):
        self.rarity = rarity
        self.points = points
    
    def calculate_price(self):
        total_price = self.PRICE_POINTS[self.rarity] + self.PRICE_POINTS[self.points]
        return total_price
        