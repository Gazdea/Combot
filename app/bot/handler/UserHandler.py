from datetime import datetime

from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

from app.bot import util
from app.bot.util import unified_command
from app.config import application
from app.config.log_execution import log_execution
from app.db import MutedUsersDTO, BanUserDTO
from app.db.di import get_muted_user_service, get_user_service, get_banned_user_service, get_user_chat_service
from app.enum import Command
from app.exception.validationExceptions import ValidationMentionUser, ValidationDatetime, ValidationQuotedText
import pytz

@unified_command(app=application, command=Command.MUTE)
@log_execution
async def user_mute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Заглушить пользователя."""
    muted_user_service = get_muted_user_service()
    user_service = get_user_service()

    message = update.message

    usernames = await util.get_mentioned_users(update, context)
    if not usernames:
        raise ValidationMentionUser

    mute_until = await util.extract_datetime_from_message(update)
    if not mute_until:
        raise ValidationDatetime

    quotes = await util.get_quoted_text(update)
    if not quotes:
        raise ValidationQuotedText

    for username in usernames:
        user = user_service.get_user_by_username(username)
        if not user:
            await message.reply_text(f'Пользователь {username} не найден.')
            continue

        muted_user_service.add_mute_user(MutedUsersDTO(user_id=user.id, chat_id=message.chat.id, time_end=mute_until, reason=quotes[0]))
        await context.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user.id,
            permissions=ChatPermissions.no_permissions(),
            until_date=mute_until
        )
        await message.reply_text(f'Пользователь {user.username} заглушен до {mute_until}')

@unified_command(app=application, command=Command.UNMUTE)
@log_execution
async def user_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Снять мут с пользователя."""
    muted_user_service = get_muted_user_service()
    user_service = get_user_service()

    message = update.message

    usernames = await util.get_mentioned_users(update, context)
    if not usernames:
        raise ValidationMentionUser

    quotes = await util.get_quoted_text(update)
    if not quotes:
        quotes = ["размучен без причины"]

    for username in usernames:
        user = user_service.get_user_by_username(username)
        if not user:
            await message.reply_text(f'Пользователь {username} не найден.')
            continue

        muted_user_service.add_mute_user(MutedUsersDTO(user_id=user.id, chat_id=message.chat.id, time_end=datetime.now(pytz.utc), reason=quotes[0]))
        await context.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user.id,
            permissions=ChatPermissions.all_permissions(),
            until_date=datetime.now(pytz.utc)
        )
        await message.reply_text(f'Пользователь {user.username} снят с мута.')

@unified_command(app=application, command=Command.KICK)
@log_execution
async def user_kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выгнать пользователя из чата."""
    banned_user_service = get_banned_user_service()
    user_service = get_user_service()

    message = update.message
    usernames = await util.get_mentioned_users(update, context)
    if not usernames:
        raise ValidationMentionUser

    quotes = await util.get_quoted_text(update)
    if not quotes:
        raise ValidationQuotedText

    for username in usernames:
        user = user_service.get_user_by_username(username)
        if not user:
            await message.reply_text(f'Пользователь {username} не найден.')
            continue

        banned_user_service.add_ban_user(BanUserDTO(user_id=user.id, chat_id=message.chat.id, time_end=datetime.now(pytz.utc), reason=quotes[0]))
        await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=user.id)
        await message.reply_text(f'Пользователь {user.username} выгнан из чата.')

@unified_command(app=application, command=Command.BAN)
@log_execution
async def user_ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Забанить пользователя."""
    banned_user_service = get_banned_user_service()
    user_service = get_user_service()
    message = update.message

    usernames = await util.get_mentioned_users(update, context)
    if not usernames:
        raise ValidationMentionUser

    mute_until = await util.extract_datetime_from_message(update)
    if not mute_until:
        raise ValidationDatetime

    quotes = await util.get_quoted_text(update)
    if not quotes:
        raise ValidationQuotedText

    for username in usernames:
        user = user_service.get_user_by_username(username)
        if not user:
            await message.reply_text(f'Пользователь {username} не найден.')
            continue

        banned_user_service.add_ban_user(BanUserDTO(user_id=user.id, chat_id=message.chat.id, time_end=mute_until, reason=quotes[0]))
        await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=user.id, until_date=mute_until)
        await message.reply_text(f'Пользователь {user.username} забанен.')

@unified_command(app=application, command=Command.UNBAN)
@log_execution
async def user_unban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Разбанить пользователя."""
    banned_user_service = get_banned_user_service()
    user_service = get_user_service()

    message = update.message
    usernames = await util.get_mentioned_users(update, context)
    if not usernames:
        raise ValidationMentionUser

    quotes =  await util.get_quoted_text(update)
    if not quotes:
        quotes = ["разбанен без причины"]

    for username in usernames:
        user = user_service.get_user_by_username(username)
        if not user:
            await message.reply_text(f'Пользователь {username} не найден.')
            continue

        banned_user_service.update_ban_user(BanUserDTO(user_id=user.id, chat_id=message.chat.id, time_end=datetime.now(pytz.utc), reason=quotes[0]))
        await context.bot.unban_chat_member(chat_id=message.chat.id, user_id=user.id)
        await message.reply_text(f'Пользователь {user.username} разбанен.')

@unified_command(app=application, command=Command.USER_INFO)
@log_execution
async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получает информацию о пользователе в чате."""
    user_chat_service = get_user_chat_service()
    user_service = get_user_service()

    message = update.message

    usernames = await util.get_mentioned_users(update, context)
    if not usernames:
        raise ValidationMentionUser

    for username in usernames:
        user = user_service.get_user_by_username(username)
        if not user:
            await message.reply_text(f'Пользователь {username} не найден.')
            continue

        user_chat = user_chat_service.get_user_chat(message.chat.id, user.id)

        await message.reply_text(f"Информация о {user.username}.\nПрисоединился: {user_chat.join_date}\nРоль: {user_chat.role}")

@unified_command(app=application, command=Command.USER_ROLE)
@log_execution
async def user_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Назначает роль пользователю."""
    user_chat_service = get_user_chat_service()
    user_service = get_user_service()
    
    message = update.message

    usernames = await util.get_mentioned_users(update, context)
    if not usernames:
        raise ValidationMentionUser

    quotes = await util.get_quoted_text(update, context)
    if not quotes:
        raise ValidationQuotedText

    for username in usernames:
        user = user_service.get_user_by_username(username)
        if not user:
            await message.reply_text(f'Пользователь {username} не найден.')
            continue
        user_chat_service.set_user_role(message.chat.id, user.id, quotes[0])
        await message.reply_text("Роль назначена пользователю.")
