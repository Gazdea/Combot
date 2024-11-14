from datetime import datetime
import random
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes

from models.DTO import BanUserDTO, MutedUsersDTO, RoleDTO
from .Util import get_mentioned_users, extract_datetime_from_message, get_quoted_text
from service import BannedUserService, ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermisionService
from resourse.bot_response import start_responses, bot_info

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Потешный старт"""
    response = random.choice(start_responses)
    await update.message.reply_text(response.format(username=update.message.from_user.username))
    
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вывод информации о боте для админа."""
    await update.message.reply_text(bot_info)

