from abc import ABC, abstractmethod
from typing import List, Optional
from app.db.model.Entity import RolePermission

from app.db.repository import BaseRepository

class RolePermissionRepository(BaseRepository, ABC):

    @abstractmethod
    def save(self, role_permission: RolePermission) -> Optional[RolePermission]:
        raise NotImplementedError()
        
    @abstractmethod
    def get(self, role_permission: RolePermission) -> Optional[RolePermission]:
        raise NotImplementedError()
        
    @abstractmethod
    def list(self) -> List[RolePermission]:
        raise NotImplementedError()
        
    @abstractmethod
    def update(self, role_permission: RolePermission) -> Optional[RolePermission]:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, role_permission: RolePermission) -> Optional[bool]:
        raise NotImplementedError()