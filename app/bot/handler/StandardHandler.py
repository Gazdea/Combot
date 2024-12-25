import random

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.util.decorators import unified_command
from app.config import application
from app.config.log_execution import log_execution
from app.db.di import get_user_chat_service
from app.resource import start_responses, bot_info
from app.enum.Enums import Command, UserRole, bot_help

@unified_command(app=application, command=Command.START)
@log_execution
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Потешный старт"""
    await update.message.reply_text(random.choice(start_responses).format(username=update.message.from_user.username))

@unified_command(app=application, command=Command.INFO)
@log_execution
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Вывод информации о боте для админа."""
    await update.message.reply_text(bot_info)

@unified_command(app=application, command=Command.HELP)
@log_execution
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получить список возможных команд"""
    user_chat_service = get_user_chat_service()
    user_chat = user_chat_service.get_user_chat(update.message.chat_id, update.message.from_user.id)
    commands = bot_help.get(user_chat.role.value)
    await update.message.reply_text(f"Доступные команды:\n"
                                    f"{commands}")

@unified_command(app=application, command=Command.FAQ)
@log_execution
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выводит FAQ."""
    await update.message.reply_text("FAQ")