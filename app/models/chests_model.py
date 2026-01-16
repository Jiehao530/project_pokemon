from pydantic import BaseModel

class Chest(BaseModel):
    name: str
    generation: int