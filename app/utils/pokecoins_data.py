from bson.objectid import ObjectId
from app.enums.currency_enum import Currency

def new_pokecoins_data(user_id: ObjectId):
    return {
        "user_id": user_id,
        "amount": 100,
        "currency": Currency.POKECOINS.value
    }