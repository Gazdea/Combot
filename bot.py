import os
import logging
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Импорт модулей приложения
from handlers.handler import Handlers

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

@dp.message_handler(commands=['start', 'help', 'mute', 'kick', 'unban', 'delete', 'info', 'ban', 'unmute'])
async def handle_command(message: types.Message):
    await Handlers(message).execute_command()

@dp.message_handler(content_types=['new_chat_members'])
async def new_member(message: types.Message):
    await Handlers(message).welcome_new_member()

@dp.message_handler()
async def handle_message(message: types.Message):
    await Handlers(message).anti_spam_protection()
    await Handlers(message).remove_links()

# ===============================
# Запуск бота
# ===============================

if __name__ == "__main__":
    try:
        asyncio.run(dp.start_polling())
        logging.info("Бот запущен.")
    except Exception as e:
        logging.error(f"Ошибка в бот-поллинге: {e}")
