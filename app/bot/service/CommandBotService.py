from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class CommandBotService(ABC):
    @abstractmethod
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def command_rename(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def commands_role(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
