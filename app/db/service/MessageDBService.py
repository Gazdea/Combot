from datetime import date, timedelta
from typing import Dict, List, Optional
from app.db.model.DTO import MessageDTO
from abc import ABC, abstractmethod

class MessageDBService(ABC):
    
    @abstractmethod
    def get_stat_user_message(self, chat_id: int, user_id: int, date_start: date = date.today(), date_end: date = date.today() + timedelta(days=1)) -> Optional[int]:
        raise NotImplementedError
    
    @abstractmethod
    def get_stats_users_message(self, chat_id: int, users_ids: List[int], date_start: date = date.today(), date_end: date = date.today() + timedelta(days=1)) -> List[Dict[int, int]]:
        raise NotImplementedError
    
    @abstractmethod
    def get_messages_by_chat_user(self, chat_id: int, user_id: int) -> Optional[list[MessageDTO]]:
        raise NotImplementedError

    @abstractmethod
    def save_message(self, message: MessageDTO) -> Optional[MessageDTO]:
        raise NotImplementedError

    @abstractmethod
    def get_top_users_by_message_count(self, chat_id: int, date_start: date = date.today(), date_end: date = date.today() + timedelta(days=1)) -> List[Dict[int, int]]:
        raise NotImplementedError