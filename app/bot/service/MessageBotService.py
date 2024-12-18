from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class MessageBotService(ABC):
    @abstractmethod
    async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    