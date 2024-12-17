from abc import ABC, abstractmethod
from typing import Optional
from app.db.model.DTO import MutedUsersDTO

class MutedUserDBService(ABC):

    @abstractmethod
    def add_mute_user(self, mute_user: MutedUsersDTO) -> Optional[MutedUsersDTO]:
        pass
    
    @abstractmethod
    def update_mute_user(self, mute_user: MutedUsersDTO) -> Optional[MutedUsersDTO]:
        pass
    
    @abstractmethod
    def get_mute_user(self, user_id: int, chat_id: int) -> Optional[MutedUsersDTO]:
        pass
