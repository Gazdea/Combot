from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from app.db.model.Entity import Message

from app.db.repository import BaseRepository

class MessageRepository(BaseRepository, ABC):

    @abstractmethod
    def get_messages(self, chat_id: int, user_id: int) -> List[Message]:
        pass
        
    @abstractmethod
    def get_count_messages(self, chat_id: int, user_id: int, date_start: date, date_end: date) -> Optional[int]:
        pass