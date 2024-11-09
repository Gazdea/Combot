from typing import List, Optional
from models.Entity import RolePermission
from .BaseRepository import BaseRepository
from config import session_scope

class RolePermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(RolePermission)
        
    def save(self, role_permission: RolePermission) -> Optional[RolePermission]:
        with session_scope() as session:
            session.merge(role_permission)
            session.commit()
            return role_permission
        
    def get(self, role_permission: RolePermission) -> Optional[RolePermission]:
        with session_scope() as session:
            return session.query(RolePermission).filter(RolePermission == role_permission).first()

    def list(self) -> List[RolePermission]:
        with session_scope() as session:
            return session.query(self.model).all()

    def update(self, role_permission: RolePermission) -> Optional[RolePermission]:
        with session_scope() as session:
            session.merge(role_permission)
            session.commit()
            return role_permission

    def delete(self, role_permission: RolePermission) -> Optional[bool]:
        with session_scope() as session:
            instance = session.query(RolePermission).filter(RolePermission == role_permission).first()
            if instance:
                session.delete(instance)
                session.commit()
                return True
            return False