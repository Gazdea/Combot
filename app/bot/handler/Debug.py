from telegram import Update
from telegram.ext import ContextTypes
from abc import ABC, abstractmethod

class Debug(ABC):
    @abstractmethod        
    async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass