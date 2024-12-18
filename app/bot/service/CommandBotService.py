from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class CommandBotService(ABC):
    @abstractmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def command_rename(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    

    @abstractmethod
    async def commands_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
