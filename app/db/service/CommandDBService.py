from typing import Optional
from app.db.model.DTO import CommandDTO
from abc import ABC, abstractmethod

class CommandDBService(ABC):

    @abstractmethod
    def rename_command(self, chat_id: int, command_name: str, new_command_name: str) -> Optional[CommandDTO]:
        pass
    
    @abstractmethod
    def get_commands_by_chat(self, chat_id: int) -> Optional[list[CommandDTO]]:
        pass
    
    @abstractmethod
    def get_command_by_chat_user_name(self, chat_id: int, user_id: int, command_name: str) -> Optional[CommandDTO]:
        pass
    
    @abstractmethod
    def get_commands_by_chat_user(self, chat_id: int, user_id: int) -> Optional[list[CommandDTO]]:
        pass
    
    @abstractmethod
    def get_commands_by_chat_role(self, chat_id: int, role_id: int) -> Optional[list[CommandDTO]]:
        pass
    
    @abstractmethod
    def get_commands_by_chat_roleName(self, chat_id: int, role_name: int) -> Optional[list[CommandDTO]]:
        pass
    
    @abstractmethod
    def get_command_by_chat_name(self, chat_id: int, command_name: str) -> Optional[CommandDTO]:
        pass