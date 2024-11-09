from .BaseRepository import BaseRepository
from config import session_scope
from typing import Optional
from models.Entity import Role, UserChat

class RoleRepository(BaseRepository):
    def __init__(self):
        super().__init__(Role)

    def get_role_by_user(self, chat_id: int, user_id: int) -> Optional[Role]:
        with session_scope() as session:
            return session.query(UserChat).filter(UserChat.chat_id == chat_id, UserChat.user_id == user_id).first().role

    def get_role_by_role_name(self, chat_id: int, role_name: str) -> Optional[Role]:
        with session_scope() as session:
            return session.query(Role).filter(Role.chat_id == chat_id, Role.role_name == role_name).first()
