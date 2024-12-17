from abc import ABC, abstractmethod
from typing import List, Optional
from app.db.model.Entity import User

from app.db.repository import BaseRepository

class UserRepository(BaseRepository, ABC):

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        pass
        
    @abstractmethod
    def get_users(self, users_ids: List[int]) -> List[User]:
        pass