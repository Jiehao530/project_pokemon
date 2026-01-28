import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helpers.pokemon_helper import get_pokemon_figure_by_chest
from models.chests_model import ChestStatus
from datetime import datetime, timedelta


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

    async def get_reward(self):
        open = self.open_chest()
        if not open:
            return None
        pokemon_figure = await get_pokemon_figure_by_chest(self.chest_generation_number)
        return pokemon_figure