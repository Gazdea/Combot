from telegram import Update, ChatMemberAdministrator, ChatMemberOwner
from telegram.ext import ContextTypes
from .Util import get_mentioned_users, extract_datetime_from_message, get_quoted_text
from service import ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermisionService

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка работоспособности бота и подключений."""
    message = update.message
    response = ["Запускаю проверку системы..."]

    # Проверка подключения к API Telegram
    try:
        bot_info = await context.bot.get_me()
        response.append(f"Подключение к API Telegram успешно.\nИмя бота: {bot_info.first_name}\nUsername: @{bot_info.username}")
    except Exception as e:
        response.append(f"Ошибка подключения к API Telegram: {str(e)}")
        await message.reply_text("\n".join(response))
        return

    # Проверка административных прав бота в чате
    try:
        chat_member = await context.bot.get_chat_member(message.chat.id, context.bot.id)
        if isinstance(chat_member, (ChatMemberAdministrator, ChatMemberOwner)):
            response.append("У бота есть административные права в этом чате.")
        else:
            response.append("У бота нет административных прав в этом чате.")
    except Exception as e:
        response.append(f"Ошибка проверки прав администратора: {str(e)}")

    # Проверка подключения к базе данных
    try:
        chat_info = ChatService().get_chat_by_id(message.chat.id)
        if chat_info:
            response.append("Подключение к базе данных успешно. Чат найден в базе данных.")
        else:
            response.append("Чат не найден в базе данных. Создаю запись.")
            ChatService().new_chat(message.chat.id, message.chat.title)
    except Exception as e:
        response.append(f"Ошибка подключения к базе данных: {str(e)}")

    # Проверка: является ли сообщение ответом на другое сообщение
    if message.reply_to_message:
        response.append("Это сообщение является ответом на другое сообщение.")
    else:
        response.append("Нет ответа на сообщение.")
    
    # Получение упомянутых пользователей, кроме бота
    users = await get_mentioned_users(update, context)
    if users:
        response.append(f"Упомянутые пользователи (кроме бота): {', '.join([str(f'{user.id} {user.username}' ) for user in users])}")
    else:
        response.append("Нет упомянутых пользователей (кроме бота).")

    # Извлечение даты и времени из сообщения
    extracted_date = await extract_datetime_from_message(update, context)
    if extracted_date:
        response.append(f"Извлечённая дата и время: {extracted_date.strftime('%d.%m.%Y %H:%M')}")
    else:
        response.append("Дата и время не указаны или не распознаны.")

    # Извлечение вложенного текста в ""
    if qoutes := await get_quoted_text(update, context):
        response.append(f"Извлеченные данные из \"\" {qoutes}")
    else:
        response.append("Извлеченных данных нету")
        
    # Отправка собранного сообщения
    response.append("Проверка завершена успешно.")
    await message.reply_text("\n".join(response))