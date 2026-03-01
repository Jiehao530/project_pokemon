def purchase_result_converter(data) -> dict:
    return {
        "item_id" : str(data["item_id"]),
        "status": data["status"],
        "currency": data["currency"]
    }

def purchase_converter(data) -> dict:
    return {
       "purchase_id": data["purchase_id"],
       "result": purchase_result_converter(data["result"]),
       "user_id": str(data["user_id"]),
       "created_at": data["created_at"] 
    }