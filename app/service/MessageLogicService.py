from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class MessageLogicService(ABC):
    @abstractmethod
    async def delete_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
    