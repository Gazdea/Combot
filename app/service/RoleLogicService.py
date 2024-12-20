from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class RoleLogicService(ABC):
    @abstractmethod
    async def role_add(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def role_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def role_command_add(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def role_command_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def role_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def role_rename(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    