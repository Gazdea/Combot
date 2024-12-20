from app.exception import ServerError, BusinessError, ValidationError, AuthenticationError
from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def global_error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Глобальный обработчик ошибок.
    """
    exception = context.error
    message = "Произошла неизвестная ошибка."

    # Определяем сообщение об ошибке в зависимости от типа исключения
    if isinstance(exception, ServerError):
        message = "Ошибка на сервере. Попробуйте позже."
    elif isinstance(exception, BusinessError):
        message = f"Ошибка бизнес-логики: {exception}"
    elif isinstance(exception, ValidationError):
        message = f"Ошибка валидации данных: {exception}"
    elif isinstance(exception, AuthenticationError):
        message = "Ошибка авторизации. Проверьте свои права доступа."
    else:
        logger.exception("Произошла неизвестная ошибка", exc_info=exception)
    
        # Логируем ошибку
    logger.error(f"Ошибка: {exception} | Update: {update}")
    
    # Отправляем сообщение пользователю, если есть обновление
    if update and update.message:
        try:
            await update.message.reply_text(message)
        except Exception as send_error:
            logger.error(f"Ошибка при отправке сообщения: {send_error}")

    # Опционально: отправить уведомление администратору
    # admin_chat_id = 123456789
    # await context.bot.send_message(chat_id=admin_chat_id, text=f"Ошибка: {exception}")
