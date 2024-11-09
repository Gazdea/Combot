from typing import Optional
from models.DTO import RolePermissionDTO
from models.Entity import RolePermission
from repository import CommandRepository, RoleRepository, RolePermissionRepository

class RolePermisionService:
    def __init__(self):
        self.command_repo = CommandRepository()
        self.role_repo = RoleRepository()
        self.role_permission_repo = RolePermissionRepository()

    def role_command_add(self, chat_id: int, role_name: str, command_name: str) -> Optional[RolePermissionDTO]:
        command = self.command_repo.get_command_by_name(chat_id, command_name)
        role = self.role_repo.get_role_by_role_name(chat_id, role_name)
        
        return RolePermissionDTO.model_validate(
            self.role_permission_repo.save(
                RolePermission(**RolePermissionDTO(
                    role_id=role.id, 
                    command_id=command.id
                    ).model_dump())
                )
            )

    def role_command_delete(self, chat_id: int, role_name: str, command_name: str) -> bool:
        command = self.command_repo.get_command_by_name(chat_id, command_name)
        role = self.role_repo.get_role_by_role_name(chat_id, role_name)
        return self.role_permission_repo.delete(RolePermission(**
                                                                     RolePermissionDTO(
                                                                         role_id=role.id, 
                                                                         command_id=command.id).model_dump()
                                                                     )
                                                )
