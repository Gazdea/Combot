from typing import List, Optional
from app.db.model.Entity import RolePermission
from sqlalchemy.orm import Session
from app.db.repository.baseImpl import RolePermissionRepository
from app.db.repository.impl import BaseRepositoryImpl

class RolePermissionRepositoryImpl(BaseRepositoryImpl[RolePermission], RolePermissionRepository):
    def __init__(self, session: Session):
        super().__init__(RolePermission, session)
        self.session: Session = session
        
    def save(self, role_permission: RolePermission) -> Optional[RolePermission]:
        self.session.merge(role_permission)
        self.session.refresh(role_permission)
        return role_permission
        
    def get(self, role_permission: RolePermission) -> Optional[RolePermission]:
        role = self.session.query(RolePermission).filter(RolePermission == role_permission).first()
        return role
        
    def list(self) -> List[RolePermission]:
        roles = self.session.query(RolePermission).all()
        return roles
        
    def update(self, role_permission: RolePermission) -> Optional[RolePermission]:
        self.session.merge(role_permission)
        self.session.refresh(role_permission)
        return role_permission

    def delete(self, role_permission: RolePermission) -> Optional[bool]:
        instance = self.session.query(RolePermission).filter(RolePermission == role_permission).first()
        if instance:
            self.session.delete(instance)
            return True
        return False