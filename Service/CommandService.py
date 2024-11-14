from typing import List, Optional
from repository import CommandRepository
from models.DTO import CommandDTO

class CommandService:
    def __init__(self):
        self.repo = CommandRepository()

    def rename_command(self, chat_id: int, command_name: str, new_command_name: str) -> Optional[CommandDTO]:
        command_dto = self.repo.get_command_by_name(chat_id, command_name)
        command_dto.command = new_command_name
        return self.repo.update(command_dto)

    def get_commands_by_chat(self, chat_id: int) -> List[CommandDTO]:
        commands = self.repo.get_commands_by_chat(chat_id)
        return [CommandDTO.model_validate(command) for command in commands]

    def get_commands_by_chat_user(self, chat_id: int, user_id: int) -> List[CommandDTO]:
        commands = self.repo.get_commands_by_chat_user(chat_id, user_id)
        return [CommandDTO.model_validate(command) for command in commands]

    def get_commands_by_chat_role(self, chat_id: int, role_id: int) -> List[CommandDTO]:
        commands = self.repo.get_commands_by_chat_role(chat_id, role_id)
        return [CommandDTO.model_validate(command) for command in commands]