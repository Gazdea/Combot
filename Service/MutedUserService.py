from typing import Optional
from models.DTO import MutedUsersDTO
from repository import MutedUserRepository

class MutedUserService:
    def __init__(self):
        self.repo = MutedUserRepository()
        
    def add_mute_user(self, mute_user: MutedUsersDTO) -> Optional[MutedUsersDTO]:
        return MutedUsersDTO.model_validate(self.repo.save(mute_user.model_dump()))
    
    def update_mute_user(self, mute_user: MutedUsersDTO) -> Optional[MutedUsersDTO]:
        return MutedUsersDTO.model_validate(self.repo.update(mute_user.model_dump()))
    
    def get_mute_user(self, user_id: int, chat_id: int) -> Optional[MutedUsersDTO]:
        return MutedUsersDTO.model_validate(self.repo.get_user_mute_by_chat_user(chat_id, user_id))
