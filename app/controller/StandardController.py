from datetime import datetime
import random
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from app.db.model.DTO import BanUserDTO, MutedUsersDTO, RoleDTO
from app.resource.bot_response import start_responses, bot_info
from app.di.ServiceDBContainer import ServiceDBContainer
from app.di.UtilContainer import UtilContainer

service_container = ServiceDBContainer
util_container = UtilContainer

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Потешный старт"""
    response = random.choice(start_responses)
    await update.message.reply_text(response.format(username=update.message.from_user.username))
    
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вывод информации о боте для админа."""
    await update.message.reply_text(bot_info)

