from typing import Optional
from models.Entity import Command, Role, RolePermission, UserChat
from .BaseRepository import BaseRepository
from config import session_scope
from sqlalchemy.orm import make_transient

class CommandRepository(BaseRepository):
    def __init__(self):
        super().__init__(Command)

    def get_command_by_name(self, chat_id: int, command_name: str) -> Optional[Command]:
        with session_scope() as session:
            command = session.query(Command).filter(
                Command.chat_id == chat_id, 
                Command.command == command_name
            ).first()
            session.expunge(command)
            make_transient(command)
            return command

    def get_commands_by_chat(self, chat_id: int) ->list[Command]:
        with session_scope() as session:
            commands = session.query(Command).filter(Command.chat_id == chat_id).all()
            for command in commands:
                session.expunge(command)
                make_transient(command)
            return commands
        
    def get_commands_by_chat_user(self, chat_id: int, user_id: int) -> list[Command]:
        with session_scope() as session:
            commands = (
                session.query(Command)
                .filter(Command.chat_id == chat_id)
                .join(RolePermission, RolePermission.command_id == Command.id)
                .join(Role, Role.id == RolePermission.role_id)
                .join(UserChat, UserChat.role_id == Role.id)
                .filter(UserChat.user_id == user_id)
                .all()
            )
            for command in commands:
                session.expunge(command)
                make_transient(command)
            return commands

    def get_commands_by_chat_role(self, chat_id: int, role_id: int) -> list[Command]:
        with session_scope() as session:
            commands = (
                session.query(Command)
                .filter(Command.chat_id == chat_id)
                .join(RolePermission, RolePermission.command_id == Command.id)
                .join(Role, Role.id == RolePermission.role_id)
                .filter(Role.id == role_id)
                .all()
            )
            for command in commands:
                session.expunge(command)
                make_transient(command)
            return commands