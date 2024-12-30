from functools import wraps
from typing import List

from telegram import Update
from telegram.ext import CallbackContext, Application, CommandHandler, MessageHandler, filters

from app.config.log_execution import log_execution
from app.db.di import get_user_chat_service
from app.enum.Enums import Command
from app.exception import AuthenticationError


@log_execution
def command_access_control(command: Command):
    """
    Проверяет права доступа пользователя на выполнение команды.
    :param command: Команда, для которой проверяются права.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
            user_chat_db_service = get_user_chat_service()
            user_chat = user_chat_db_service.get_user_chat(
                update.effective_chat.id, update.effective_user.id
            )
            allowed_roles =  command.allowed_roles
            if user_chat.role not in allowed_roles:
                raise AuthenticationError(f"У вас нет доступа к {command.value} команде.")
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

@log_execution
def register_command(app: Application, command: Command):
    """
    Регистрирует команду как обработчик.
    :param app: Экземпляр Application.
    :param command: Команда, для которой регистрируется хендлер.
    """
    def decorator(func):
        for cmd in command.triggers:
            handler = CommandHandler(cmd, func)
            app.add_handler(handler)
        return func
    return decorator

@log_execution
def unified_command(app: Application, command: Command):
    """
    Общий декоратор для проверки прав доступа и регистрации команды.
    :param app: Экземпляр Application.
    :param command: Команда, для которой выполняются действия.
    """
    def decorator(func):
        func = command_access_control(command)(func)
        func = register_command(app, command)(func)
        return func
    return decorator

@log_execution
def register_message_handler(app: Application, filters: filters.BaseFilter, **kwargs):
    """
    Декоратор для регистрации текстовых обработчиков с несколькими фильтрами.
    :param app: Экземпляр Application.
    :param filters: Перечень фильтров, которые должны применяться к хендлеру.
    """
    def decorator(func):
        handler = MessageHandler(filters, func, **kwargs)
        app.add_handler(handler)
        return func
    return decorator