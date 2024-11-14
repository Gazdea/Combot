import re
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from models.DTO import MessageDTO, UserDTO
from service import ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermisionService
from .Util import get_mentioned_users, extract_datetime_from_message, get_quoted_text

async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет сообщение из чата."""
    message = update.message
    if message.reply_to_message:
        await context.bot.delete_message(message.chat.id, message.message_id)
        await context.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    else:
        await message.reply_text('Необходимо указать, какое сообщение вы хотите удалить.')

