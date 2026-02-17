from app.enums.rarity_enum import Rarity

GENERATION_RANGES = {
    1: [1, 151], 
    2: [152, 251], 
    3: [252, 386], 
    }

RARITY_OPTIONS = [Rarity.COMMON.value, Rarity.RARE.value, Rarity.EPIC.value, Rarity.LEGENDARY.value]
POINT_OPTIONS = [1, 2, 3, 4, 5]

POINT_WEIGHTS_FOR_CHESTS = [46, 33, 15, 5, 1]
RARITY_WEIGHTS_FOR_CHESTS = [50, 35, 10, 5]
