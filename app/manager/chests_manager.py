import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helpers.pokemon_helper import search_pokemon
from models.pokemon_model import Rarity
from models.chests_model import ChestStatus
from datetime import datetime, timedelta
import random

class ChestsManager:
    MAX_CHESTS = 6
    GENERATION_TIME = timedelta(hours=4)

    def __init__(self, chest: int, last_generation: datetime, next_chest):
        self.chest = chest
        self.last_generation = last_generation
        self.next_chest = next_chest
    
    def update_chest_status(self):
        now = datetime.utcnow()
        time_elapsed = now - self.last_generation
        chest_generation = time_elapsed // self.GENERATION_TIME
        
        if chest_generation > 0:
            self.chest = min(self.MAX_CHESTS, self.chest + chest_generation)
            self.last_generation = now - (time_elapsed % self.GENERATION_TIME)
        if self.chest >= self.MAX_CHESTS:
            self.next_chest = None
        else:
            self.next_chest = self.last_generation + self.GENERATION_TIME
    
    def open_chest(self):
        self.update_chest_status()
        if self.chest <= 0:
            return False
        self.chest -= 1
        return True

    def model_cheststatus(self) -> ChestStatus:
        return ChestStatus(chest=self.chest, last_generated=self.last_generation, next_chest=self.next_chest)

class RewardChestManager(ChestsManager):
    def __init__(self, chest: int, last_generation: datetime, next_chest, chest_generation_number: int):
        super().__init__(chest, last_generation, next_chest)
        self.chest_generation_number = chest_generation_number
    
    async def get_pokemon(self):
        if self.chest_generation_number == 1:
            number = random.randint(1, 151)
        elif self.chest_generation_number == 2:
            number = random.randint(152, 251)
        elif self.chest_generation_number == 3:
            number = random.randint(252, 386)

        pokemon = await search_pokemon(number)
        return pokemon
    
    def get_rarity_and_point_pokemon(self):
        rarity_options = [Rarity.COMMON.value, Rarity.RARE.value, Rarity.EPIC.value, Rarity.LEGENDARY.value]
        rarity_weights = [50, 35, 10, 5]
        rarity = random.choices(rarity_options, weights=rarity_weights, k=1)[0]
        point_options = [1, 2, 3, 4, 5]
        point_weights = [46, 33, 15, 5, 1]
        point = random.choices(point_options, weights=point_weights, k=1)[0]
        return [rarity, point]

    async def get_reward(self):
        open = self.open_chest()
        if not open:
            return None
        pokemon = await self.get_pokemon()
        rarity, points = self.get_rarity_and_point_pokemon()
        return {
            "number": pokemon.number,
            "name": pokemon.name,
            "type": pokemon.type,
            "generation": pokemon.generation,
            "rarity": rarity,
            "points": points
            }