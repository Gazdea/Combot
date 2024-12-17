from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from app.db.model.Entity import UserChat

from app.db.repository import BaseRepository

class UserChatRepository(BaseRepository, ABC):

    @abstractmethod
    def delete(self, chat_id: int, user_id: int) -> bool:
        pass
        
    @abstractmethod
    def get(self, chat_id: int, user_id: int) -> Optional[UserChat]:
        pass        

    @abstractmethod
    def get_join_users(self, chat_id: int, date_start: date, date_end: date) -> List[UserChat]:
        pass