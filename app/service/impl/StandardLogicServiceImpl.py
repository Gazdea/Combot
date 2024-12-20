from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class StandardLogicServiceImpl(ABC):
    @abstractmethod
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()