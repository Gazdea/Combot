from telegram import Update
from telegram.ext import ContextTypes

from app.bot.service import StandardBotService

class StandardBotServiceImpl(StandardBotService):
    def __init__(self):
        super().__init__()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()