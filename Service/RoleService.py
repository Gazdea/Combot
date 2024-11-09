from models.DTO import RoleDTO
from models.Entity import Role
from repository import RoleRepository
from typing import Optional

class RoleService:
    def __init__(self):
        self.repo = RoleRepository()

    def add_role(self, role: RoleDTO) -> Optional[RoleDTO]:
        return RoleDTO.model_validate(self.repo.save(Role(**role.model_dump())))

    def delete_role(self, chat_id: int, role_name: str) -> bool:
        role = self.repo.get_role_by_role_name(chat_id, role_name)
        return self.repo.delete(role.id) if role else False

    def get_role_by_chat_user(self, chat_id: int, user_id: int) -> Optional[RoleDTO]:
        role = self.repo.get_role_by_user(chat_id, user_id)
        return RoleDTO.model_validate(role)
