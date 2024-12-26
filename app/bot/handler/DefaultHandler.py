import re
from app.bot.util.decorators import register_message_handler
from app.db.di import get_muted_user_service, get_chat_service, get_user_chat_service, get_user_service, \
    get_message_service
from app.db.model.DTO import MessageDTO, UserDTO
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes, filters
from app.config import  application
from app.enum import UserRole
from app.exception import ServerError


@register_message_handler(app=application, filters=filters.TEXT & ~filters.COMMAND)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(chat_id=update.message.chat_id, user_id=update.message.from_user.id)
    await save_message(update, context)
    if member.status not in ['administrator', 'creator']:
        await remove_pattern(update, context)
        await anti_spam_protection(update, context)

async def anti_spam_protection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Защита от спама: если пользователь отправляет больше max_messages за time_window секунд, он заглушается."""
    message = update.message
    muted_user_service = get_muted_user_service()
    if mute_user := muted_user_service.get_active_mute_user(message.chat.id, message.from_user.id):
        await context.bot.restrict_chat_member(
            chat_id=mute_user.chat_id,
            user_id=mute_user.user_id,
            permissions=ChatPermissions.no_permissions(),
            until_date=mute_user.time_end
        )

async def remove_pattern(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Удаляет сообщения, содержащие ссылки."""
    message = update.message
    chat_service = get_chat_service()
    chat_dto = chat_service.get_chat_by_id(message.chat.id)
    if re.search(chat_dto.delete_pattern, message.text):
        await context.bot.delete_message(message.chat.id, message.message_id)

@register_message_handler(app=application, filters=filters.StatusUpdate.NEW_CHAT_MEMBERS)
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветствие новых пользователей в чате. Если бот добавлен в чат, добавляет информацию о чате и администраторах."""
    message = update.message
    bot_added = False
    chat_service = get_chat_service()
    user_service = get_user_service()
    user_chat_service = get_user_chat_service()

    for member in message.new_chat_members:
        if member.id == context.bot.id:
            bot_added = True
        else:
            user = user_service.add_user(UserDTO(id=member.id, username=member.username))
            user_chat_service.add_user_by_chat(member.id, message.chat.id, UserRole.USER, message.date)
            await context.bot.send_message(message.chat.id,
                                           f'Добро пожаловать в наш чат, {member.username or member.first_name}!')

    if bot_added:
        chat_service.new_chat(message.chat.id, message.chat.title)
        admins = await context.bot.get_chat_administrators(message.chat.id)
        for admin in admins:
            user_service.add_user(UserDTO(id=admin.user.id, username=admin.user.username))
            user_chat_service.add_user_by_chat(admin.user.id, message.chat.id, UserRole.ADMIN, message.date)
        await context.bot.send_message(message.chat.id, 'Спасибо, что пригласили меня. Теперь я готов работать!')
        await context.bot.send_message(message.chat.id,
                                       'Для корректной работы с чатом не забудьте установить права администратора.')

async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сохранение сообщения"""
    message = update.message
    user_service = get_user_service()
    user_chat_service = get_user_chat_service()
    message_service = get_message_service()

    user = user_service.get_user_by_id(message.from_user.id)
    if not user:
        await message.reply_text("Кто ты воин, дай как запишу тебя")
        user_service.add_user(UserDTO(id=message.from_user.id, username=message.from_user.username))
    user_chat = user_chat_service.get_user_chat(message.chat.id, message.from_user.id)
    if not user_chat:
        user_chat_service.add_user_by_chat(message.from_user.id, message.chat.id, 'user', message.date)

    message_service.save_message(
        MessageDTO(
            message_id=message.message_id,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            message=message.text,
            date=message.date
        )
    )
