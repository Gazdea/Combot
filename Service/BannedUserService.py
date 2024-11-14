from typing import Optional
from models.DTO import BanUserDTO
from repository import BannedUserRepository

class BannedUserService:
    def __init__(self):
        self.repo = BannedUserRepository()
        
    def add_ban_user(self, ban_user: BanUserDTO) -> Optional[BanUserDTO]:
        return BanUserDTO.model_validate(self.repo.save(ban_user.model_dump()))
    
    def update_ban_user(self, ban_user: BanUserDTO) -> Optional[BanUserDTO]:
        return BanUserDTO.model_validate(self.repo.update(ban_user.model_dump()))
    
    def get_ban_user(self, user_id: int, chat_id: int) -> Optional[BanUserDTO]:
        return BanUserDTO.model_validate(self.repo.get_user_ban_by_chat_user(chat_id, user_id))
