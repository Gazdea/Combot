from telegram import Update
from telegram.ext import ContextTypes

from app.bot.service import UserBotService

class UserBotServiceImpl(UserBotService):
    def __init__(self):
        super().__init__()

    async def user_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def user_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def user_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def user_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def user_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()

    async def user_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError()
    