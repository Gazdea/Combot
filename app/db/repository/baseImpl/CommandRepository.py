from abc import ABC, abstractmethod
from typing import List, Optional
from app.db.model.Entity import Command

from app.db.repository.BaseRepository import BaseRepository

class CommandRepository(BaseRepository, ABC):

    @abstractmethod
    def get_command_by_name(self, chat_id: int, command_name: str) -> Optional[Command]:
        raise NotImplementedError()

    @abstractmethod
    def get_command_by_chat_user_command_name(self, chat_id: int, user_id: int, command_name: str) -> Optional[Command]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_commands_by_chat(self, chat_id: int) ->List[Command]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_commands_by_chat_user(self, chat_id: int, user_id: int) -> List[Command]:
        raise NotImplementedError()

    @abstractmethod
    def get_commands_by_chat_role(self, chat_id: int, role_id: str) -> List[Command]:
        raise NotImplementedError()
        
    @abstractmethod
    def get_commands_by_chat_roleName(self, chat_id: int, role_name: str) -> List[Command]:
        raise NotImplementedError()