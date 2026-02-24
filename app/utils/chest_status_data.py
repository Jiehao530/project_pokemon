from bson.objectid import ObjectId
from datetime import datetime, timedelta

def new_chest_status_data(user_id: ObjectId) -> dict:
    return {
            "user_id": user_id,
            "chest": 1,
            "last_generated": datetime.utcnow(),
            "next_chest": datetime.utcnow() + timedelta(hours=4)
        }