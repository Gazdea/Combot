from telegram import Update
from telegram.ext import ContextTypes

from app.bot.service import RoleBotService

class RoleBotServiceImpl(RoleBotService):
    def __init__(self):
        super().__init__()

    async def role_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    
    async def role_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def role_command_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def role_command_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def role_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def role_rename(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    