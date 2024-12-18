from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class RoleBotService(ABC):
    @abstractmethod
    async def role_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def role_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def role_command_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def role_command_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def role_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def role_rename(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    