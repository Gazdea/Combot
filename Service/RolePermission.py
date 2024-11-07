from typing import Optional
from Models.DTO import RolePermissionDTO
from Repository import CommandRepository, RolePermission, RoleRepository, RolePermissionRepository

class RolePermisionService:
    def __init__(self):
        self.command_repo = CommandRepository()
        self.role_repo = RoleRepository()
        self.role_permission_repo = RolePermissionRepository()

    def role_command_add(self, chat_id: int, role_name: str, command_name: str) -> Optional[RolePermissionDTO]:
        command = self.command_repo.get_command_by_name(chat_id, command_name)
        role = self.role_repo.get_role_by_role_name(chat_id, role_name)
        
        return RolePermissionDTO.model_validate(
            self.role_permission_repo.create(
                RolePermission(**RolePermissionDTO(
                    role_id=role.id, 
                    command_id=command.id
                    ))
                )
            )

    def role_command_delete(self, chat_id: int, role_name: str, command_name: str) -> bool:
        command = self.command_repo.get_command_by_name(chat_id, command_name)
        role = self.role_repo.get_role_by_role_name(chat_id, role_name)
        
        role_permission_dto = RolePermissionDTO(role_id=role.id, command_id=command.id)
        return self.role_permission_repo.delete(role_permission_dto)
