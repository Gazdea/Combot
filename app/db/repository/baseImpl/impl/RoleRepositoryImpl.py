from typing import List, Optional
from app.db.model.Entity import Role, UserChat
from sqlalchemy.orm import Session
from app.db.repository.baseImpl import RoleRepository
from app.db.repository.impl import BaseRepositoryImpl

class RoleRepositoryImpl(BaseRepositoryImpl[Role], RoleRepository):
    def __init__(self, session: Session):
        super().__init__(Role, session)
        self.session: Session = session

    def get_roles_by_chat(self, chat_id: int) -> List[Role]:
        roles = self.session.query(Role).filter(Role.chat_id == chat_id).all()
        return roles

    def get_role_by_user(self, chat_id: int, user_id: int) -> Optional[Role]:
        role = self.session.query(UserChat).filter(UserChat.chat_id == chat_id, UserChat.user_id == user_id).first().role
        return role
        
    def get_role_by_role_name(self, chat_id: int, role_name: str) -> Optional[Role]:
        role = self.session.query(Role).filter(Role.chat_id == chat_id, Role.role_name == role_name).first()
        return role
    