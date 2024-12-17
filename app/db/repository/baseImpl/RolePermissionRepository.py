from abc import ABC, abstractmethod
from typing import List, Optional
from app.db.model.Entity import RolePermission

from app.db.repository import BaseRepository

class RolePermissionRepository(BaseRepository, ABC):

    @abstractmethod
    def save(self, role_permission: RolePermission) -> Optional[RolePermission]:
        pass
        
    @abstractmethod
    def get(self, role_permission: RolePermission) -> Optional[RolePermission]:
        pass
        
    @abstractmethod
    def list(self) -> List[RolePermission]:
        pass
        
    @abstractmethod
    def update(self, role_permission: RolePermission) -> Optional[RolePermission]:
        pass

    @abstractmethod
    def delete(self, role_permission: RolePermission) -> Optional[bool]:
        pass