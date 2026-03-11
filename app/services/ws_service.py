from fastapi import WebSocket
from app.dependencies.ws_auth_depends import get_current_user_for_ws
from app.memory.exchange_rooms_memory import EXCHANGE_ROOMS
from app.enums.exchange_type_enum import ExchangeType
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
    
    async def exchange_ws(self, wedsocket: WebSocket, exchange_id: str):
        await WebSocket.accept()
        exchange_room = EXCHANGE_ROOMS.get(exchange_id)
        if not exchange_room:
            wedsocket.send_json({ExchangeType.ERROR.value: "Exchange Room Not Found"})
            wedsocket.close()
            return

        auth_header = wedsocket.headers.get("authorization")
        if not auth_header:
            wedsocket.send_json({ExchangeType.ERROR.value: "Missing Authorization Header"})
            wedsocket.close()
            return
        
        token_type, _ , token = auth_header.partition(" ")
        if token_type.lower() != "bearer":
            wedsocket.send_json({ExchangeType.ERROR.value: "Incorrect Token Type"})
            wedsocket.close()
            return
        
        user = await get_current_user_for_ws(token)
        if not user:
            wedsocket.send_json({ExchangeType.ERROR.value: "Invalid Token"})
            wedsocket.close()
            return