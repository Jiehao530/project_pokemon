from fastapi import HTTPException, status
from app.db.repositories.chests_repository import ChestsRepository
from app.managers.chests_manager import ChestsManager, RewardChestManager
from app.utils.id_converter import id_converter
from app.utils.chest_status_data import new_chest_status_data
from app.schemes.users_scheme import User

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

    async def get_cheststatus(self, user: User):
        objectid_user_id = id_converter(user.id)
        search = await ChestsRepository.search_chest_status("user_id", objectid_user_id)
        if not search:
            insert_chest_status = await ChestsRepository.insert_chest_status(new_chest_status_data(objectid_user_id))
            if not insert_chest_status:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insert Chest Status Error")
            new_status = await ChestsRepository.search_chest_status("user_id", objectid_user_id)
            return {"chest_status": new_status}

        chests_manager = ChestsManager(search.chest, search.last_generated, search.next_chest)
        chests_manager.update_chest_status()
        chest_status = chests_manager.get_cheststatus_scheme()
        await ChestsRepository.update_chest_status(objectid_user_id, chest_status.model_dump())
        
        return {"chest_status": chest_status}
          
    async def open_chest(self, chest_id: str, user: User):
        chest_dict = await self.get_chest(chest_id)
        chest_status_dict = await self.get_cheststatus(user)

        chest = chest_dict["chest"]
        chest_status = chest_status_dict["chest_status"]

        reward_chest_manager = RewardChestManager(chest_status.chest, chest_status.last_generated, chest_status.next_chest, chest.generation)
        reward = reward_chest_manager.get_reward()
        if reward is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You haven't chests available")
        
        update_data = reward_chest_manager.get_cheststatus_scheme().model_dump()
        update = ChestsRepository.update_chest_status(id_converter(user.id), update_data)
        if not update:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update Chest Status Error")
