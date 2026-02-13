from fastapi import HTTPException, status
from app.db.repositories.chests_repository import ChestsRepository

class ChestsService:

    async def get_chests(self):
        search_chests = await ChestsRepository.search_chests()
        if not search_chests:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There aren't chests")
        return {"chests": search_chests}

    async def get_chest(self, chest_id: str):
        search_chest = await ChestsRepository.search_chest("_id", chest_id)
        if not search_chest:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chest not found")
        return {"chest": search_chest}
    
    async def get_chest_id(self, chest_name: str):
        search_chest_id = await ChestsRepository.search_chest("name", chest_name)
        if not search_chest_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chest not found")
        return {"chest_id": search_chest_id.id}
