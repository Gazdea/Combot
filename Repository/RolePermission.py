from typing import Optional
from Models.Entity import RolePermission
from Repository.Base import BaseRepository
from config import session_scope

class RolePermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(RolePermission)