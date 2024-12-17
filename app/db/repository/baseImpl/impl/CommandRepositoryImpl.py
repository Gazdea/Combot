from typing import List, Optional
from app.db.model.Entity import Command, Role, RolePermission, UserChat
from app.db.repository.baseImpl import CommandRepository
from sqlalchemy.orm import Session
from app.db.repository.impl import BaseRepositoryImpl

class CommandRepositoryImpl(BaseRepositoryImpl[Command], CommandRepository):
    def __init__(self, session: Session):
        super().__init__(Command, session)
        self.session: Session = session

    def get_command_by_name(self, chat_id: int, command_name: str) -> Optional[Command]:
        if command := self.session.query(Command).filter(
            Command.chat_id == chat_id, 
            Command.command == command_name
        ).first():
            return command
        return None

    def get_command_by_chat_user_name(self, chat_id: int, user_id: int, command_name: str) -> Optional[Command]:
        if command := (
            self.session.query(Command)
            .filter(Command.chat_id == chat_id)
            .join(RolePermission, RolePermission.command_id == Command.id)
            .join(Role, Role.id == RolePermission.role_id)
            .join(UserChat, UserChat.role_id == Role.id)
            .filter(UserChat.user_id == user_id, Command.command == command_name)
            .first()
        ):
            return command
        return None
    
    def get_commands_by_chat(self, chat_id: int) -> List[Command]:
        commands = self.session.query(Command).filter(Command.chat_id == chat_id).all()
        return commands
        
    def get_commands_by_chat_user(self, chat_id: int, user_id: int) -> List[Command]:
        commands = (
            self.session.query(Command)
            .filter(Command.chat_id == chat_id)
            .join(RolePermission, RolePermission.command_id == Command.id)
            .join(Role, Role.id == RolePermission.role_id)
            .join(UserChat, UserChat.role_id == Role.id)
            .filter(UserChat.user_id == user_id)
            .all()
        )
        return commands

    def get_commands_by_chat_role(self, chat_id: int, role_id: int) -> List[Command]:
        commands = (
            self.session.query(Command)
            .filter(Command.chat_id == chat_id)
            .join(RolePermission, RolePermission.command_id == Command.id)
            .join(Role, Role.id == RolePermission.role_id)
            .filter(Role.id == role_id)
            .all()
        )
        return commands
        
    def get_commands_by_chat_roleName(self, chat_id: int, role_name: str) -> List[Command]:
        commands = (
            self.session.query(Command)
            .filter(Command.chat_id == chat_id)
            .join(RolePermission, RolePermission.command_id == Command.id)
            .join(Role, Role.id == RolePermission.role_id)
            .filter(Role.role_name == role_name)
            .all()
        )
        return commands