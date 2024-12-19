from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Optional
from app.db.model.DTO import UserChatDTO

class UserChatDBService(ABC):

    @abstractmethod
    def get_user_chat(self, chat_id: int, user_id: int) -> Optional[UserChatDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_stats_users_join(self, chat_id: int, date_start: date = date.today(), date_end: date = date.today()) -> Optional[list[UserChatDTO]]:
        raise NotImplementedError()

    @abstractmethod
    def set_user_role(self, chat_id: int, user_id: int, role_name: str) -> Optional[UserChatDTO]:
        raise NotImplementedError()

    @abstractmethod
    def add_user_by_chat(self, user_id: int, chat_id: int, role_name: str, join_date: datetime) -> Optional[UserChatDTO]:
        raise NotImplementedError()

    @abstractmethod        
    def delete_user_chat(self, chat_id: int, user_id: int) -> Optional[bool]:
        raise NotImplementedError()