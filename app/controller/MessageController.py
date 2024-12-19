import re
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from app.db.model.DTO import MessageDTO, UserDTO
from app.di.ServiceDBContainer import ServiceDBContainer
from app.di.UtilContainer import UtilContainer

service_container = ServiceDBContainer
util_container = UtilContainer


async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет сообщение из чата."""
    message = update.message
    if message.reply_to_message:
        await context.bot.delete_message(message.chat.id, message.message_id)
        await context.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    else:
        await message.reply_text('Необходимо указать, какое сообщение вы хотите удалить.')

