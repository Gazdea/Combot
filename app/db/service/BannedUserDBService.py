from typing import Optional
from app.db.model.DTO import BanUserDTO
from abc import ABC, abstractmethod

class BannedUserDBService(ABC):
        
    @abstractmethod
    def add_ban_user(self, ban_user: BanUserDTO) -> Optional[BanUserDTO]:
        raise NotImplementedError()
    
    @abstractmethod
    def update_ban_user(self, ban_user: BanUserDTO) -> Optional[BanUserDTO]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_ban_user(self, user_id: int, chat_id: int) -> Optional[BanUserDTO]:
        raise NotImplementedError()