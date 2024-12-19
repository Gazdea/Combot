from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class StandardBotService(ABC):
    @abstractmethod
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()