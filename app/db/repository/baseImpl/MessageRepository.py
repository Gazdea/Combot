from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, Any

from sqlalchemy import Row

from app.db.model.Entity import Message

from app.db.repository import BaseRepository

class MessageRepository(BaseRepository, ABC):

    @abstractmethod
    def get_messages(self, chat_id: int, user_id: int) -> List[Message]:
        raise NotImplementedError()
        
    @abstractmethod
    def get_count_messages(self, chat_id: int, user_id: int, date_start: date, date_end: date) -> Optional[int]:
        raise NotImplementedError()

    @abstractmethod
    def get_top_users_by_message_count(self, chat_id: int, date_start: date, date_end: date) -> List[
        Row[tuple[Any, Any]]]:
        raise NotImplementedError()