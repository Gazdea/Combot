import re
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from models.DTO import MessageDTO, UserDTO
from service import ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermisionService
from .Util import get_mentioned_users, extract_datetime_from_message, get_quoted_text

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить список возможных команд"""
    message = update.message
    if available_commands := CommandService().get_commands_by_chat_user(
        message.chat.id, message.from_user.id
    ):
        commands = "\n".join([f"{cmd.command} - {cmd.description}" for cmd in available_commands])
        await message.reply_text(commands)

async def command_rename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Переименовывает команду."""
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes[0] and not quotes[1]:
        await message.reply_text('Необходимо указать название команды, и новое название. \"command\" \"new command\"')
        return
    CommandService().rename_command(message.chat.id, quotes[0], quotes[1])
    await message.reply_text("Команда переименована.")
    
async def get_commands_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать роль.')
        return
    role = RoleService().get_role_by_chat_name(message.chat.id, quotes[0])
    if not role:
        await message.reply_text("Роль не найдена.")
        return
    if available_commands := CommandService().get_commands_by_chat_role(
        message.chat.id, message.from_user.id
    ):
        commands = "\n".join([f"{cmd.command} - {cmd.description}" for cmd in available_commands])
        await message.reply_text(commands)
    else:
        await message.reply_text("У данной роли нет доступных команд.")
