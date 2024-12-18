from telegram import Update
from telegram.ext import ContextTypes

from app.bot.service import CommandBotService

class CommandBotServiceImpl(CommandBotService):
    def __init__(self):
        super().__init__()
        
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def command_rename(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    async def commands_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
