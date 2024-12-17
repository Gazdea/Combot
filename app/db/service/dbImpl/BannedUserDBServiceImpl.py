from typing import Optional
from app.db.model.DTO import BanUserDTO
from app.db.service import BannedUserDBService
from app.db.repository.baseImpl.BannedUserRepository import BannedUserRepository

class BannedUserDBServiceImpl(BannedUserDBService):
    def __init__(self, repo: BannedUserRepository):
        self.repo = repo
        
    def add_ban_user(self, ban_user: BanUserDTO) -> Optional[BanUserDTO]:
        if ban_user := self.repo.save(ban_user.model_dump()): 
            return BanUserDTO.model_validate(ban_user)
        return None
    
    def update_ban_user(self, ban_user: BanUserDTO) -> Optional[BanUserDTO]:
        if ban_user := self.repo.save(ban_user.model_dump()): 
            return BanUserDTO.model_validate(ban_user)
        return None
    
    def get_ban_user(self, user_id: int, chat_id: int) -> Optional[BanUserDTO]:
        if ban_user := self.repo.get_user_ban_by_chat_user(chat_id, user_id): 
            return BanUserDTO.model_validate(ban_user)
        return None