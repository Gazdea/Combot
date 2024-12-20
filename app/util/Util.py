from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple
from telegram import Update
from telegram.ext import ContextTypes
from app.db.model.DTO import CommandDTO, UserDTO

class Util(ABC):

    @abstractmethod
    async def get_mentioned_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    async def get_quoted_text(self, update: Update) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    async def extract_datetime_from_message(self, update: Update) -> Optional[datetime] | None:
        raise NotImplementedError