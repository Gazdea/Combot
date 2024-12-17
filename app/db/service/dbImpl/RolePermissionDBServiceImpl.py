from typing import Optional
from app.db.model.DTO import RolePermissionDTO
from app.db.model.Entity import RolePermission
from app.db.repository.baseImpl import CommandRepository, RoleRepository, RolePermissionRepository
from app.db.service import RolePermissionDBService

class RolePermissionDBServiceImpl(RolePermissionDBService):
    def __init__(self, command_repo: CommandRepository, role_repo: RoleRepository, role_permission_repo: RolePermissionRepository):
        self.command_repo = command_repo
        self.role_repo = role_repo
        self.role_permission_repo = role_permission_repo

    def role_command_add(self, chat_id: int, role_name: str, command_name: str) -> Optional[RolePermissionDTO]:
        if command := self.command_repo.get_command_by_name(chat_id, command_name):
            if role := self.role_repo.get_role_by_role_name(chat_id, role_name):
                if role_permission := self.role_permission_repo.save(
                        RolePermission(**RolePermissionDTO(
                            role_id=role.id, 
                            command_id=command.id
                            ).model_dump())
                        ):
                    return RolePermissionDTO.model_validate(role_permission)
        return None

    def role_command_delete(self, chat_id: int, role_name: str, command_name: str) -> Optional[bool]:
        if command := self.command_repo.get_command_by_name(chat_id, command_name):
            if role := self.role_repo.get_role_by_role_name(chat_id, role_name):
                if role_permission := self.role_permission_repo.delete(RolePermission(**
                                                                     RolePermissionDTO(
                                                                         role_id=role.id, 
                                                                         command_id=command.id).model_dump()
                                                                     )
                                                ):
                    return role_permission
        return None
