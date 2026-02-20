from bson.objectid import ObjectId

def new_pokecoins_data(user_id: ObjectId):
    return {
        "user_id": user_id,
        "amount": 100,
        "currency": "pokecoins"
    }