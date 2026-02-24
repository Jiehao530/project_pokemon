from fastapi import HTTPException, status
from bson.objectid import ObjectId

def id_converter(id: str):
    try:
        return ObjectId(id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
