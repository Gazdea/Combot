from abc import ABC, abstractmethod
from typing import Optional
from app.db.model.DTO import RoleDTO

class RoleDBService(ABC):

    @abstractmethod
    def add_role(self, role: RoleDTO) -> Optional[RoleDTO]:
        raise NotImplementedError()

    @abstractmethod
    def delete_role(self, chat_id: int, role_name: str) -> Optional[bool]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_role_by_chat_user(self, chat_id: int, user_id: int) -> Optional[RoleDTO]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_role_by_chat_name(self, chat_id: int, role_name: str) -> Optional[RoleDTO]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_roles_by_chat(self, chat_id: int) -> Optional[list[RoleDTO]]:
        raise NotImplementedError()
    
    @abstractmethod
    def role_rename(self, role_name: str, new_role_name: str) -> Optional[RoleDTO]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, role_id: int) -> Optional[bool]:
        raise NotImplementedError()