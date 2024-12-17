from datetime import datetime
from typing import List, Optional
from app.db.model.Entity import BanUser
from abc import ABC, abstractmethod

from app.db.repository import BaseRepository

class BannedUserRepository(BaseRepository, ABC):
    
    @abstractmethod
    def get_users_ban_by_chat(self, chat_id: int) -> List[BanUser]:
        pass
        
    @abstractmethod
    def get_user_bans_by_chats(self, user_id: int) -> List[BanUser]:
        pass
    
    @abstractmethod
    def get_user_ban_by_chat_user(self, chat_id: int, user_id: int, start_time: datetime, end_time: datetime) -> Optional[BanUser]:
        pass
        