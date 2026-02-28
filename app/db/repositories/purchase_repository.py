from app.db.repositories.collections import purchase_collection
from app.schemes.purchase_scheme import Purchase
from app.converters.purchase_converter import purchase_converter

class PurchaseRepository:

    @staticmethod
    async def search_purchase(field: str, value):
        purchase = await purchase_collection.find_one({field: value})
        return Purchase(**purchase_converter(purchase)) if purchase else None