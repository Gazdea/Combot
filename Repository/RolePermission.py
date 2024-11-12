from typing import Optional
from models.Entity import RolePermission
from .BaseRepository import BaseRepository
from config import session_scope
from sqlalchemy.orm import make_transient

class RolePermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(RolePermission)
        
    def save(self, role_permission: RolePermission) -> Optional[RolePermission]:
        with session_scope() as session:
            session.merge(role_permission)
            session.refresh(role_permission)
            session.expunge(role_permission)
            make_transient(role_permission)
            return role_permission
        
    def get(self, role_permission: RolePermission) -> Optional[RolePermission]:
        with session_scope() as session:
            role = session.query(RolePermission).filter(RolePermission == role_permission).first()
            session.expunge(role)
            make_transient(role_permission)
            return role
        
    def list(self) -> list[RolePermission]:
        with session_scope() as session:
            roles = session.query(self.model).all()
            for role in roles:
                session.expunge(role)
                make_transient(role)
            return roles
        
    def update(self, role_permission: RolePermission) -> Optional[RolePermission]:
        with session_scope() as session:
            session.merge(role_permission)
            session.refresh(role_permission)
            session.expunge(role_permission)
            make_transient(role_permission)
            return role_permission

    def delete(self, role_permission: RolePermission) -> Optional[bool]:
        with session_scope() as session:
            instance = session.query(RolePermission).filter(RolePermission == role_permission).first()
            if instance:
                session.delete(instance)
                return True
            return False