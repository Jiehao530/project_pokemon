from app.memory.exchange_rooms_memory import EXCHANGE_ROOMS
from app.schemes.users_scheme import User
from uuid import uuid4

class WedsocketService:

    async def create_exchange_room(self, user: User):
        exchange_id = uuid4()
        data_room = {
            "creator": user.id,
            "participant": None,
            "connections": [],
            "exchange": {"item_offered": {}, "item_wanted": {}, "status": {}}
        }
        EXCHANGE_ROOMS[exchange_id] = data_room
        return {"exchange_id": exchange_id}