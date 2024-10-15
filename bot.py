import os
import logging
import asyncio
from Connection.SQLAlchemy import DBConnection
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Импорт модулей приложения
from Handler.Handler import Handlers

# Загрузка переменных окружения
load_dotenv()

# Получение токена и ID админа
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

if not TOKEN:
    logging.error("Токен бота не установлен. Проверьте переменные окружения.")
    exit(1)

# Создание объектов бота и диспетчера
bot = Bot(TOKEN)
dp = Dispatcher(bot)

# ===============================
# Обработчики команд
# ===============================

@dp.message_handler(lambda message: message.text.startswith('/'))
async def handle_command(message: types.Message):
    await Handlers().execute_command(message)

@dp.message_handler(content_types=['new_chat_members'])
async def new_member(message: types.Message):
    await Handlers().welcome_new_member(message)

@dp.message_handler()
async def handle_message(message: types.Message):
    """"""
    # await Handlers().anti_spam_protection(message)
    await Handlers().remove_links(message)

# ===============================
# Запуск бота
# ===============================

if __name__ == "__main__":
    try:
        asyncio.run(dp.start_polling())
        logging.info("Бот запущен.")
    except Exception as e:
        logging.error(f"Ошибка в бот-поллинге: {e}")
