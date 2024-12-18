from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class StandardBotService(ABC):
    @abstractmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()