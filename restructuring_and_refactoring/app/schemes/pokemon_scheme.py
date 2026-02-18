from pydantic import BaseModel
from typing import List

class Pokemon(BaseModel):
    id: int
    number: int
    name: str
    type: List[str]
    generation: int