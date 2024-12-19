from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class Handler(ABC):
    
    @abstractmethod
    async def get_method_from_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """handler он указывает какой контроллер надо вызвать"""
        pass

    @abstractmethod        
    async def anti_spam_protection(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Защита от спама: если пользователь отправляет больше max_messages за time_window секунд, он заглушается."""
        pass
    
    @abstractmethod
    async def remove_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удаляет сообщения, содержащие ссылки."""
        pass

    @abstractmethod
    async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Приветствие новых пользователей в чате. Если бот добавлен в чат, добавляет информацию о чате и администраторах."""
        pass

    @abstractmethod
    async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Сохранение сообщения"""
        pass
