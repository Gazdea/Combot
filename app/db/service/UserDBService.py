from abc import ABC, abstractmethod
from typing import Optional
from app.db.model.DTO import UserDTO

    
class UserDBService(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        pass

    @abstractmethod    
    def get_user_by_username(self, username: int) -> Optional[UserDTO]:
        pass

    @abstractmethod    
    def add_user(self, user: UserDTO) -> Optional[UserDTO]:
        pass