from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from app.bot import util
from app.bot.util import unified_command
from app.config import application
from app.config.log_execution import log_execution
from app.db.di import get_message_service, get_chat_service, get_user_chat_service, get_user_service
from app.enum import Command
from datetime import  date

from app.exception.validationExceptions import ValidationQuotedText


@unified_command(app=application, command=Command.CHAT_USER_JOIN)
async def chat_user_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отображает статистику присоединения пользователя к чату."""
    user_chat_service = get_user_chat_service()
    user_service = get_user_service()

    date_start = await util.extract_datetime_from_message(update)
    if not date_start:
        date_start = date.today()
    else:
        date_start = date_start.date()

    users = user_chat_service.get_stats_users_join(chat_id=update.message.chat.id, date_start=date_start)
    if not users:
        await update.message.reply_text(f"Нет данных о присоединении пользователей к чату от {date_start}.")
        return

    response = [
        (user_service.get_user_by_id(user.user_id).username, user.join_date) for user in users
    ]
    response_text = f"Статистика присоединения пользователей к чату от {date_start}:\n" + "\n".join(
        f"{username}: {join_date}" for username, join_date in response
    )
    await update.message.reply_text(response_text)

@unified_command(app=application, command=Command.CHAT_USER_ACTIVE)
async def chat_user_active(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отображает статистику активности пользователя в чате."""
    message_service = get_message_service()
    user_service = get_user_service()

    date_start = await util.extract_datetime_from_message(update)
    if not date_start:
        date_start = date.today()
    else:
        date_start = date_start.date()

    usernames = await util.get_mentioned_usernames(update, context)

    if not usernames:
        top_messages = message_service.get_top_users_by_message_count(chat_id=update.message.chat.id, date_start=date_start)
        users = [user_service.get_user_by_id(user_id) for user_id, _ in top_messages]
        response = [
            (user.username, message_count)
            for user, message_count in zip(users, [count for _, count in top_messages])
        ]
    else:
        users = user_service.get_users_by_usernames(usernames)
        response = [
            (user.username, message_service.get_stat_user_message(chat_id=update.message.chat.id, user_id=user.id, date_start=date_start))
            for user in users
        ]

    response_text = f"Статистика активности пользователей в чате от {date_start}:\n" + "\n".join(
        f"{username}: {message_count}" for username, message_count in response
    )

    await update.message.reply_text(response_text)

@unified_command(app=application, command=Command.CHAT_SPAM_MUTE_TIME)
@log_execution
async def chat_spam_mute_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Устанавливает время мьюта за спам для чата."""
    chat_service = get_chat_service()
    message = update.message

    quotes = await util.get_quoted_text(update)

    if not quotes:
        chat =  chat_service.get_chat_by_id(message.chat.id)
        await message.reply_text(f"Текущее время мьюта за спам: {chat.spam_mute_time} минут\n"
                                 f"Для изменения напишите \"10\" - 10 минут'")
        return

    if not quotes[0].isdigit():
        raise ValidationQuotedText('Необходимо указать время мьюта за спам. \"10\" - 10 минут')

    chat_service.update_spam_mute_time(message.chat_id, int(quotes[0]))

    await message.reply_text("Время мьюта за спам установлено.")

@unified_command(app=application, command=Command.CHAT_SPAM_MESSAGE)
@log_execution
async def chat_spam_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Устанавливает количество сообщений для срабатывания антиспам защиты."""
    chat_service = get_chat_service()
    message = update.message

    quotes = await util.get_quoted_text(update)

    if not quotes:
        chat =  chat_service.get_chat_by_id(message.chat.id)
        await message.reply_text(f"Текущее количество сообщений для антиспам: {chat.spam_message} сообщений\n"
                                 f"Для изменения напишите \"10\" - 10 сообщений'")
        return

    if not quotes[0].isdigit():
        raise ValidationQuotedText('Необходимо указать количество сообщений для антиспам защиты. \"10\" - 10 сообщений')

    chat_service.update_spam_message(message.chat.id, int(quotes[0]))
    await message.reply_text("Число сообщений для антиспам установлено.")

@unified_command(app=application, command=Command.CHAT_DELETE_PATTERN)
@log_execution
async def chat_delete_pattern(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Устанавливает шаблон для автоматического удаления сообщений."""
    chat_service = get_chat_service()
    
    message = update.message
    quotes = await util.get_quoted_text(update)

    if not quotes:
        chat =  chat_service.get_chat_by_id(message.chat.id)
        await message.reply_text(f"Текущий шаблон для удаления сообщений: {chat.delete_pattern}\n"
                                 f"Для изменения напишите \"http[s]?://\S+|www\.\S+\" - паттерн удаления ссылок")
        return

    chat_service.update_delete_pattern(message.chat.id, quotes[0])

    await message.reply_text("Шаблон удаления сообщений установлен.")


