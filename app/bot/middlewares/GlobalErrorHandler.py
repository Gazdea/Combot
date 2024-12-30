import httpx

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
        message = f"Ошибка бизнес-логики:\n{exception}"
    elif isinstance(exception, ValidationError):
        message = f"Ошибка валидации данных:\n{exception}"
    elif isinstance(exception, AuthenticationError):
        message = "Ошибка авторизации. Проверьте свои права доступа."
    elif isinstance(exception, httpx.ReadError):
        logger.exception("Ошибка с связью: возможно ложная ошибка", exc_info=exception)
    else:
        logger.exception("Произошла неизвестная ошибка", exc_info=exception)

    logger.error(f"Ошибка: {exception} | Update: {update}")

    if update and update.message:
        try:
            await update.message.reply_text(message)
        except Exception as send_error:
            logger.error(f"Ошибка при отправке сообщения: {send_error}")


    # admins = await context.bot.get_chat_administrators(update.message.chat.id)
    # for admin in admins:
    #     await admin.user.send_message(f"Ошибка: {exception}")
