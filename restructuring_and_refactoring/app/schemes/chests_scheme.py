from pydantic import BaseModel

class Chest(BaseModel):
    id: str
    name: str
    generation: int