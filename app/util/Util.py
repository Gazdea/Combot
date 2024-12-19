from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple
from telegram import Update
from telegram.ext import ContextTypes
from app.db.model.DTO import CommandDTO, UserDTO

class Util(ABC):

    @abstractmethod
    async def get_mentioned_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> List[UserDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_quoted_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    async def extract_datetime_from_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def check_methods(self, classes, chat_id: int, user_id: int) -> List[Tuple[CommandDTO, Tuple[str, str]]]:
        raise NotImplementedError

    @abstractmethod
    def method_search(self, classes, method_name: str) -> Tuple[str, str]:
        raise NotImplementedError
