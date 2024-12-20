from abc import ABC, abstractmethod
from typing import Dict, List
from telegram import Update
from telegram.ext import ContextTypes

from app.db.model.DTO import UserChatDTO
from app.dto import BotResponse

class ChatBotService(ABC):
    @abstractmethod
    async def chat_user_join(self, update: Update, context: ContextTypes.DEFAULT_TYPE, users_chat: List[UserChatDTO]) -> BotResponse:
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_user_active(self, update: Update, context: ContextTypes.DEFAULT_TYPE, users: Dict[str, int]) -> BotResponse:
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_spam_mute_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> BotResponse:
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_spam_num_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> BotResponse:
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_spam_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> BotResponse:
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_delete_pattern(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> BotResponse:
        raise NotImplementedError()
