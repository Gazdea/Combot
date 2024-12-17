from abc import ABC, abstractmethod
from typing import Optional
from app.db.model.DTO import RolePermissionDTO

class RolePermissionDBService(ABC):

    @abstractmethod
    def role_command_add(self, chat_id: int, role_name: str, command_name: str) -> Optional[RolePermissionDTO]:
        pass

    @abstractmethod
    def role_command_delete(self, chat_id: int, role_name: str, command_name: str) -> Optional[bool]:
        pass
