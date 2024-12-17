from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from app.db.model.DTO import MessageDTO, UserDTO
from app.di import ServiceContainer, UtilContainer

service_container = ServiceContainer
util_container = UtilContainer

async def chat_user_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает статистику присоединения пользователя к чату."""
    user_chat_service = service_container.user_chat_service()
    
    message = update.message
    user_chat = user_chat_service.get_stats_users_join(message.chat.id)
    if not user_chat:
        await message.reply_text("Пользователи не присоединились.")
        return
    await message.reply_text(f"За сегодня приспоединилось к чату: {user_chat}")

async def chat_user_active(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает статистику активности пользователя в чате."""
    bot_util = util_container.bot_util()
    message_service = service_container.message_service()
    
    message = update.message
    users = await bot_util.get_mentioned_users(update, context)
    if not users:
        await message.reply_text('Необходимо указать пользователя. \"@username\"')
        return
    for user in users:
        count_messages = message_service.get_stat_user_message(message.chat.id, user.id)
        await message.reply_text(f"Информация о {user.username}.\nЗа сегодня написал: {count_messages}")

async def chat_spam_mute_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Устанавливает время мьюта за спам для чата."""
    bot_util = util_container.bot_util()
    chat_service = service_container.chat_service()
    
    message = update.message
    quotes = await bot_util.get_quoted_text(update, context)
    if not quotes or not quotes[0].isdigit():
        await message.reply_text('Необходимо указать время мьюта за спам. \"10\" - 10 минут")')
        return
    chat = chat_service.get_chat_by_id(message.chat.id)
    chat.spam_mute_time = int(quotes[0])
    chat_service.update_chat(chat)
    await message.reply_text("Время мьюта за спам установлено.")

async def chat_spam_num_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Устанавливает количество сообщений для срабатывания антиспам защиты."""
    bot_util = util_container.bot_util()
    chat_service = service_container.chat_service()
    
    message = update.message
    quotes = await bot_util.get_quoted_text(update, context)
    if not quotes or not quotes[0].isdigit():
        await message.reply_text('Необходимо указать кол-во сообщений для мута. \"10\"')
        return
    chat = chat_service.get_chat_by_id(message.chat.id)
    chat.spam_message = int(quotes[0])
    chat_service.update_chat(chat)
    await message.reply_text("Число сообщений для антиспам установлено.")

async def chat_spam_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Устанавливает время, в течение которого считается количество сообщений для антиспам защиты."""
    bot_util = util_container.bot_util()
    chat_service = service_container.chat_service()
    
    message = update.message
    quotes = await bot_util.get_quoted_text(update, context)
    if not quotes or not quotes[0].isdigit():
        await message.reply_text('Необходимо указать время в течении которого считается кол-во сообщений. \"10\"')
        return
    chat = chat_service.get_chat_by_id(message.chat.id)
    chat.spam_time = int(quotes[0])
    chat_service.update_chat(chat)
    await message.reply_text("Время антиспам защиты установлено.")

async def chat_delete_pattern(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Устанавливает шаблон для автоматического удаления сообщений."""
    bot_util = util_container.bot_util()
    chat_service = service_container.chat_service()
    
    message = update.message
    quotes = await bot_util.get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать паттерн для удаления сообщений. \"http[s]?://\S+|www\.\S+\"')
        return
    chat = chat_service.get_chat_by_id(message.chat.id)
    chat.delete_pattern = quotes[0]
    chat_service.update_chat(chat)
    await message.reply_text("Шаблон удаления сообщений установлен.")


