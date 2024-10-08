import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Импорт модулей приложения
from db.connection import DBConnectionPool, get_user_role
from handlers.admin import Admin
from handlers.moderator import Moderator
from handlers.user import User
from handlers.bot import BotHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)

# Загрузка переменных окружения
load_dotenv()

# Получение токена и ID админа
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

if not TOKEN:
    logging.error("Токен бота не установлен. Проверьте переменные окружения.")
    exit(1)

# Инициализация пула соединений
DBConnectionPool.initialize()

# Создание объектов бота и диспетчера
bot = Bot(TOKEN)  # Исправлено здесь
dp = Dispatcher(bot)

# Функция уведомления админа
async def notify_admin(message):
    if ADMIN_CHAT_ID:
        await bot.send_message(ADMIN_CHAT_ID, message)
    else:
        logging.warning("ADMIN_CHAT_ID не установлен. Невозможно отправить сообщение админу.")

# ===============================
# Фабрика обработчиков по ролям
# ===============================
class HandlerFactory:
    @staticmethod
    async def get_handler(message: types.Message):
        """Возвращает обработчик на основе роли пользователя"""
        user_id = message.from_user.id
        role = await get_user_role(user_id)
        
        if role == 'admin':
            return Admin()
        elif role == 'moderator':
            return Moderator()
        elif role == 'user':
            return User()
        else:
            await handler_bot.welcome_new_member(message)
            return None

handler_bot = BotHandler()

# ===============================
# Обработчики команд
# ===============================
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    handler = await HandlerFactory.get_handler(message)
    if handler:
        await handler.start(message)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    handler = await HandlerFactory.get_handler(message)
    if handler:
        await handler.help(message)

@dp.message_handler(commands=['info'])
async def info_command(message: types.Message):
    handler = await HandlerFactory.get_handler(message)
    if handler:
        await handler.info(message)

@dp.message_handler(commands=['kick'])
async def kick_user_command(message: types.Message):
    handler = await HandlerFactory.get_handler(message)
    if handler:
        await handler.kick(message)

@dp.message_handler(commands=['mute'])
async def mute_command(message: types.Message):
    handler = await HandlerFactory.get_handler(message)
    if handler:
        await handler.mute(message)

@dp.message_handler(commands=['unmute'])
async def unmute_command(message: types.Message):
    handler = await HandlerFactory.get_handler(message)
    if handler:
        await handler.unmute(message)

@dp.message_handler(commands=['ban'])
async def ban_command(message: types.Message):
    handler = await HandlerFactory.get_handler(message)
    if handler:
        await handler.ban(message)

@dp.message_handler(commands=['unban'])
async def unban_command(message: types.Message):
    handler = await HandlerFactory.get_handler(message)
    if handler:
        await handler.unban(message)

@dp.message_handler(commands=['delete'])
async def delete_message_command(message: types.Message):
    handler = await HandlerFactory.get_handler(message)
    if handler:
        await handler.delete_message(message)

@dp.message_handler(content_types=['new_chat_members'])
async def welcome_new_member(message: types.Message):
    await handler_bot.welcome_new_member(message)

@dp.message_handler()
async def handle_message(message: types.Message):
    await handler_bot.anti_spam_protection(message)
    await handler_bot.remove_links(message)

# ===============================
# Запуск бота
# ===============================
async def on_startup(dp):
    await DBConnectionPool.initialize()

if __name__ == "__main__":
    try:
        logging.info("Бот запущен.")
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except Exception as e:
        logging.error(f"Ошибка в бот-поллинге: {e}")
