from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class UserLogicServiceImpl(ABC):
    @abstractmethod
    async def user_mute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def user_unmute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def user_kick(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def user_ban(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def user_unban(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def user_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def user_role(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    