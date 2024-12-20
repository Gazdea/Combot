from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from app.db.model.DTO import MessageDTO, UserDTO
from app.di.ServiceLogicContainer import ServiceLogicContainer
from app.exception.validationExceptions import ValidationMentionUser

service_logic_chat = ServiceLogicContainer

async def chat_user_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отображает статистику присоединения пользователя к чату."""
    chat_logic_service = service_logic_chat.chat_logic_service()
    
    update.message.reply_text(chat_logic_service.chat_user_join(update, context))
    
async def chat_user_active(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отображает статистику активности пользователя в чате."""
    # util = util_container.util()
    # message_service = service_db_container.message_service()
    # chat_bot_service = service_bot_container.chat_bot_service()
    
    # users = await util.get_mentioned_users(update, context)
    # users_ids = [user.id for user in users]
    # counts_messages = message_service.get_stats_users_message(update.message.chat.id, users_ids)
    
    # chat_bot_service.chat_user_active(update, context, )

async def chat_spam_mute_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Устанавливает время мьюта за спам для чата."""
    # bot_util = util_container.bot_util()
    # chat_service = service_db_container.chat_service()
    
    # message = update.message
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes or not quotes[0].isdigit():
    #     await message.reply_text('Необходимо указать время мьюта за спам. \"10\" - 10 минут")')
    #     return
    # chat = chat_service.get_chat_by_id(message.chat.id)
    # chat.spam_mute_time = int(quotes[0])
    # chat_service.update_chat(chat)
    # await message.reply_text("Время мьюта за спам установлено.")

async def chat_spam_num_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Устанавливает количество сообщений для срабатывания антиспам защиты."""
    # bot_util = util_container.bot_util()
    # chat_service = service_db_container.chat_service()
    
    # message = update.message
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes or not quotes[0].isdigit():
    #     await message.reply_text('Необходимо указать кол-во сообщений для мута. \"10\"')
    #     return
    # chat = chat_service.get_chat_by_id(message.chat.id)
    # chat.spam_message = int(quotes[0])
    # chat_service.update_chat(chat)
    # await message.reply_text("Число сообщений для антиспам установлено.")

async def chat_spam_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Устанавливает время, в течение которого считается количество сообщений для антиспам защиты."""
    # bot_util = util_container.bot_util()
    # chat_service = service_db_container.chat_service()
    
    # message = update.message
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes or not quotes[0].isdigit():
    #     await message.reply_text('Необходимо указать время в течении которого считается кол-во сообщений. \"10\"')
    #     return
    # chat = chat_service.get_chat_by_id(message.chat.id)
    # chat.spam_time = int(quotes[0])
    # chat_service.update_chat(chat)
    # await message.reply_text("Время антиспам защиты установлено.")

async def chat_delete_pattern(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Устанавливает шаблон для автоматического удаления сообщений."""
    # bot_util = util_container.bot_util()
    # chat_service = service_db_container.chat_service()
    
    # message = update.message
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes:
    #     await message.reply_text('Необходимо указать паттерн для удаления сообщений. \"http[s]?://\S+|www\.\S+\"')
    #     return
    # chat = chat_service.get_chat_by_id(message.chat.id)
    # chat.delete_pattern = quotes[0]
    # chat_service.update_chat(chat)
    # await message.reply_text("Шаблон удаления сообщений установлен.")


