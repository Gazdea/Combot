import re
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from models.DTO import MessageDTO, UserDTO
from service import ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermisionService
from .Util import get_mentioned_users, extract_datetime_from_message, get_quoted_text

async def chat_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает информацию о пользователе в чате."""
    message = update.message
    users = await get_mentioned_users(update, context)
    if not users:
        await message.reply_text('Необходимо указать пользователя. \"@username\"')
        return
    for user in users:
        stat_user = UserChatService().get_user_chat(message.chat.id, user.id)
        role = RoleService().get_role_by_chat_user(message.chat.id, user.id)
        await message.reply_text(f"Информация о {user.username}.\nПрисоединился: {stat_user.join_date}\nРоль: {role.role_name}")

async def chat_stats_user_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает статистику присоединения пользователя к чату."""
    message = update.message
    user_chat = UserChatService().get_stats_users_join(message.chat.id)
    if not user_chat:
        await message.reply_text("Пользователи не присоединились.")
        return
    await message.reply_text(f"За сегодня приспоединилось к чату: {user_chat}")

async def chat_stats_user_active(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает статистику активности пользователя в чате."""
    message = update.message
    users = await get_mentioned_users(update, context)
    if not users:
        await message.reply_text('Необходимо указать пользователя. \"@username\"')
        return
    for user in users:
        count_messages = MessageService().get_stat_user_message(message.chat.id, user.id)
        await message.reply_text(f"Информация о {user.username}.\nЗа сегодня написал: {count_messages}")

async def chat_spam_mute_time_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Устанавливает время мьюта за спам для чата."""
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes or not quotes[0].isdigit():
        await message.reply_text('Необходимо указать время мьюта за спам. \"10\" - 10 минут")')
        return
    chat = ChatService().get_chat_by_id(message.chat.id)
    chat.spam_mute_time = int(quotes[0])
    ChatService().update_chat(chat)
    await message.reply_text("Время мьюта за спам установлено.")

async def chat_spam_num_message_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Устанавливает количество сообщений для срабатывания антиспам защиты."""
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes or not quotes[0].isdigit():
        await message.reply_text('Необходимо указать кол-во сообщений для мута. \"10\"')
        return
    chat = ChatService().get_chat_by_id(message.chat.id)
    chat.spam_message = int(quotes[0])
    ChatService().update_chat(chat)
    await message.reply_text("Число сообщений для антиспам установлено.")

async def chat_spam_time_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Устанавливает время, в течение которого считается количество сообщений для антиспам защиты."""
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes or not quotes[0].isdigit():
        await message.reply_text('Необходимо указать время в течении которого считается кол-во сообщений. \"10\"')
        return
    chat = ChatService().get_chat_by_id(message.chat.id)
    chat.spam_time = int(quotes[0])
    ChatService().update_chat(chat)
    await message.reply_text("Время антиспам защиты установлено.")

async def chat_delete_pattern_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Устанавливает шаблон для автоматического удаления сообщений."""
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать паттерн для удаления сообщений. \"http[s]?://\S+|www\.\S+\"')
        return
    chat = ChatService().get_chat_by_id(message.chat.id)
    chat.delete_pattern = quotes[0]
    ChatService().update_chat(chat)
    await message.reply_text("Шаблон удаления сообщений установлен.")


