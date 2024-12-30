from telegram import Update
from telegram.ext import ContextTypes

from app.bot.util import unified_command
from app.config import application
from app.enum import Command
from app.exception.validationExceptions import ValidationMessage


@unified_command(app=application, command=Command.DELETE_MESSAGE)
async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Удаляет сообщение из чата."""
    message = update.message
    if message.reply_to_message:
        await context.bot.delete_message(message.chat.id, message.message_id)
        await context.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    else:
        raise ValidationMessage