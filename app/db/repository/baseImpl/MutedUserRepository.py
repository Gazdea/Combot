from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from app.db.model.Entity import MutedUser

from app.db.repository import BaseRepository

class MutedUserRepository(BaseRepository, ABC):
        
    @abstractmethod
    def get_users_mute_by_chat(self, chat_id: int) -> List[MutedUser]:
        raise NotImplementedError()
        
    @abstractmethod
    def get_user_mutes_by_chats(self, user_id: int) -> List[MutedUser]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_user_mute_by_chat_user(self, chat_id: int, user_id: int, start_time: datetime, end_time: datetime) -> Optional[MutedUser]:
        raise NotImplementedError()
