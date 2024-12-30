import random

from telegram import Update
from telegram.ext import ContextTypes

from app.bot import util
from app.bot.util.decorators import unified_command
from app.config import application
from app.config.log_execution import log_execution
from app.db.di import get_user_chat_service
from app.resource import start_responses, bot_info
from app.enum.Enums import Command, UserRole, bot_help
from app.resource.bot_response import faq_responses


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

    quotes = await util.get_quoted_text(update)
    if quotes:
        command_trigger = quotes[0].lower()
        for command in commands:
            if command_trigger in command["triggers"]:
                response = (
                    f"Команда: /{command_trigger}\n"
                    f"{command['full_description']}"
                )
                await update.message.reply_text(response)
                return
        await update.message.reply_text("Команда не найдена.")
    else:
        response = ["Список команд:"]
        for command in commands:
            response.append(f"/{', /'.join(command['triggers'])}: {command['short_description']}")
        await update.message.reply_text("\n".join(response))


@unified_command(app=application, command=Command.FAQ)
@log_execution
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выводит FAQ."""
    await update.message.reply_text(random.choice(faq_responses))