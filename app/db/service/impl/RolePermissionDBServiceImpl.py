from typing import Optional
from app.db.model.DTO import RolePermissionDTO
from app.db.model.Entity import RolePermission
from app.db.repository.baseImpl import RolePermissionRepository
from app.db.service import RolePermissionDBService

class RolePermissionDBServiceImpl(RolePermissionDBService):
    def __init__(self, role_permission_repo: RolePermissionRepository):
        self.role_permission_repo = role_permission_repo

    def role_command_add(self, chat_id: int, role_name: str, command_name: str) -> Optional[RolePermissionDTO]:
        if role_permission := self.role_permission_repo.save(
                RolePermission(**RolePermissionDTO(
                    role_name=role_name, 
                    command_name=command_name
                    ).model_dump())
                ):
            return RolePermissionDTO.model_validate(role_permission)
        return None

    def role_command_delete(self, chat_id: int, role_name: str, command_name: str) -> Optional[bool]:
        if role_permission := self.role_permission_repo.delete(RolePermission(**
                                                                RolePermissionDTO(
                                                                    role_name=role_name, 
                                                                    command_name=command_name).model_dump()
                                                                )
                                        ):
            return role_permission
        return None
