from abc import ABC, abstractmethod
from typing import List, Optional
from app.db.model.Entity import Role

from app.db.repository import BaseRepository

class RoleRepository(BaseRepository, ABC):

    @abstractmethod
    def get_roles_by_chat(self, chat_id: int) -> List[Role]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_role_by_user(self, chat_id: int, user_id: int) -> Optional[Role]:
        raise NotImplementedError()
        
    @abstractmethod
    def get_role_by_role_name(self, chat_id: int, role_name: str) -> Optional[Role]:
        raise NotImplementedError()
    