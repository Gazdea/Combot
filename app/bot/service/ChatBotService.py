from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class ChatBotService(ABC):
    @abstractmethod
    async def chat_user_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_user_active(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_spam_mute_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_spam_num_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_spam_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    @abstractmethod
    async def chat_delete_pattern(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
