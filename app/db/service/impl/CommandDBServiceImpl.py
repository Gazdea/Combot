from typing import Optional
from app.db.repository.baseImpl import CommandRepository, RoleRepository
from app.db.model.DTO import CommandDTO
from app.db.service import CommandDBService

class CommandDBServiceImpl(CommandDBService):
    def __init__(self, command_repo: CommandRepository):
        self.repo = command_repo

    def rename_command(self, chat_id: int, command_name: str, new_command_name: str) -> Optional[CommandDTO]:
        if command := self.repo.get_command_by_name(chat_id, command_name):
            command.command = new_command_name
            if command := self.repo.save(command):
                return CommandDTO.model_validate(command)
        return None

    def get_commands_by_chat(self, chat_id: int) -> Optional[list[CommandDTO]]:
        if commands := self.repo.get_commands_by_chat(chat_id):
            return [CommandDTO.model_validate(command) for command in commands]
        return None
        
    def get_command_by_chat_user_command_name(self, chat_id: int, user_id: int, command_name: str) -> Optional[CommandDTO]:
        if command := self.repo.get_command_by_chat_user_command_name(chat_id, user_id, command_name):
            return command
        raise Exception("Метод не найден")

    def get_commands_by_chat_user(self, chat_id: int, user_id: int) -> Optional[list[CommandDTO]]:
        if commands := self.repo.get_commands_by_chat_user(chat_id, user_id):
            return [CommandDTO.model_validate(command) for command in commands]
        return None

    def get_commands_by_chat_role(self, chat_id: int, role_id: int) -> Optional[list[CommandDTO]]:
        if commands := self.repo.get_commands_by_chat_role(chat_id, role_id):
            return [CommandDTO.model_validate(command) for command in commands]
        return None
    
    def get_commands_by_chat_roleName(self, chat_id: int, role_name: str) -> Optional[list[CommandDTO]]:
        # if role := self.role_repo.get_role_by_role_name(chat_id, role_name):
        if commands := self.repo.get_commands_by_chat_role(chat_id, role_name):
            return [CommandDTO.model_validate(command) for command in commands]
        return None
    
    def get_command_by_chat_name(self, chat_id: int, command_name: str) -> Optional[CommandDTO]:
        if command := self.repo.get_command_by_name(chat_id, command_name):
            return CommandDTO.model_validate(command)
        return None