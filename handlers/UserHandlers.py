from datetime import datetime
import re
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from models.DTO import BanUserDTO, MessageDTO, UserDTO, MutedUsersDTO
from service import BannedUserService, ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermisionService
from .Util import get_mentioned_users, extract_datetime_from_message, get_quoted_text

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Заглушить пользователя."""
    message = update.message
    users = await get_mentioned_users(update, context)
    if not users:
        await message.reply_text('Необходимо указать пользователей, которых нужно заглушить. Пример @Username')
        return
    mute_until = await extract_datetime_from_message(update, context)
    if not mute_until:
        await message.reply_text('Необходимо указать время заглушки. Пример 2001-01-01 или 01:01 или 1h, 1m, 1d, 1w или все вместе')
        return
    quotes = await get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать причину заглушки. Пример \"Нам такой не нужен\"')
        return
    for user in users:
        MutedUserService().add_mute_user(MutedUsersDTO(user_id=user.id, chat_id=message.chat.id, until_date=mute_until, reason=quotes[0]))
        await context.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user.id,
            permissions=ChatPermissions.no_permissions(),
            until_date=mute_until
        )
        await message.reply_text(f'Пользователь {user.username} заглушен до {mute_until}')

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Снять мут с пользователя."""
    message = update.message
    users = await get_mentioned_users(update, context)
    if not users:
        await message.reply_text('Необходимо указать пользователей, с которых нужно снять мут. Пример @Username')
        return
    for user in users:
        MutedUserService().update_mute_user(MutedUsersDTO(user_id=user.id, chat_id=message.chat.id, until_date=datetime.now()))
        await context.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user.id,
            permissions=ChatPermissions.all_permissions(),
            until_date=datetime.now()
        )

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выгнать пользователя из чата."""
    message = update.message
    users = await get_mentioned_users(update, context)
    if not users:
        await message.reply_text('Необходимо указать пользователей, которых нужно заглушить. Пример @Username')
        return
    quotes = await get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать причину заглушки. Пример \"Нам такой не нужен\"')
        return
    for user in users:
        BannedUserService().add_ban_user(BanUserDTO(user_id=user.id, chat_id=message.chat.id, until_date=datetime.now(), reason=quotes[0]))
        await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=user.id)
        await message.reply_text(f'Пользователь {user.username} выгнан из чата.')

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Забанить пользователя."""
    message = update.message
    users = await get_mentioned_users(update, context)
    if not users:
        await message.reply_text('Необходимо указать пользователей, которых нужно заглушить. Пример @Username')
        return
    mute_until = await extract_datetime_from_message(update, context)
    if not mute_until:
        await message.reply_text('Необходимо указать время заглушки. Пример 2001-01-01 или 01:01 или 1h, 1m, 1d, 1w или все вместе')
        return
    quotes = await get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать причину заглушки. Пример \"Нам такой не нужен\"')
        return
    for user in users:
        BannedUserService().add_ban_user(BanUserDTO(user_id=user.id, chat_id=message.chat.id, until_date=mute_until, reason=quotes[0]))
        await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=user.id, until_date=mute_until)
        await message.reply_text(f'Пользователь {user.username} забанен.')

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Разбанить пользователя."""
    message = update.message
    users = await get_mentioned_users(update, context)
    if not users:
        await message.reply_text('Необходимо указать пользователя, которого нужно разбанить. Пример @Username')
        return
    for user in users:
        BannedUserService().update_ban_user(BanUserDTO(user_id=user.id, chat_id=message.chat.id, until_date=datetime.now()))
        await context.bot.unban_chat_member(chat_id=message.chat.id, user_id=user.id)
        await message.reply_text(f'Пользователь {user.username} разбанен.')
