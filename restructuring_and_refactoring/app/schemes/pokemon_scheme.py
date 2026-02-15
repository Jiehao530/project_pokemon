from pydantic import BaseModel
from typing import List

class Pokemon(BaseModel):
    id: str
    number: int
    name: str
    type: List[str]
    generation: int