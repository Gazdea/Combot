from typing import Optional
from app.db.model.DTO import RoleDTO
from app.db.model.Entity import Role
from app.db.repository.baseImpl import RoleRepository
from app.db.service import RoleDBService

class RoleDBServiceImpl(RoleDBService):
    def __init__(self, role_repo: RoleRepository):
        self.repo = role_repo

    def add_role(self, role: RoleDTO) -> Optional[RoleDTO]:
        if role := self.repo.save(Role(**role.model_dump())):
            return RoleDTO.model_validate(role)
        return None

    def delete_role(self, chat_id: int, role_name: str) -> Optional[bool]:
        if role := self.repo.get_role_by_role_name(chat_id, role_name):
            if role := self.repo.delete(role.id):
                return role
        return None
    
    def get_role_by_chat_user(self, chat_id: int, user_id: int) -> Optional[RoleDTO]:
        if role := self.repo.get_role_by_user(chat_id, user_id):
            return RoleDTO.model_validate(role)
        return None
    
    def get_role_by_chat_name(self, chat_id: int, role_name: str) -> Optional[RoleDTO]:
        if role := self.repo.get_role_by_role_name(chat_id, role_name):
            return RoleDTO.model_validate(role)
        return None
    
    def get_roles_by_chat(self, chat_id: int) -> Optional[list[RoleDTO]]:
        if roles := self.repo.get_roles_by_chat(chat_id):
            return [RoleDTO.model_validate(role) for role in roles]
        return None
    
    def role_rename(self, role_name: str, new_role_name: str) -> Optional[RoleDTO]:
        if role := self.repo.get_role_by_role_name(role_name=role_name):
            role.role_name = new_role_name
            if role := self.repo.save(role):
                return RoleDTO.model_validate(role)
        return None
    
    def delete(self, role_id: int) -> Optional[bool]:
        if role := self.repo.delete(role_id):
            return role
        return None