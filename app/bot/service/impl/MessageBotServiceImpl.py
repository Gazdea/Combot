from telegram import Update
from telegram.ext import ContextTypes

from app.bot.service import MessageBotService

class MessageBotServiceImpl(MessageBotService):
    def __init__(self):
        super().__init__()

    async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    