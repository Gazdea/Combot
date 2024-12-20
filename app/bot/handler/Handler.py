from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class Handler(ABC):
    
    @abstractmethod
    async def get_method_from_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """handler он указывает какой контроллер надо вызвать"""
        pass

    @abstractmethod        
    async def anti_spam_protection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Защита от спама: если пользователь отправляет больше max_messages за time_window секунд, он заглушается."""
        pass
    
    @abstractmethod
    async def remove_links(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Удаляет сообщения, содержащие ссылки."""
        pass

    @abstractmethod
    async def welcome_new_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Приветствие новых пользователей в чате. Если бот добавлен в чат, добавляет информацию о чате и администраторах."""
        pass

    @abstractmethod
    async def save_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Сохранение сообщения"""
        pass
