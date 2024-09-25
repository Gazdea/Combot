import telebot
import os
from db.connection import DBConnectionPool, get_user_role
from handlers.admin import handle_start as admin_start, handle_add_moderator, handle_remove_user
from handlers.moderator import handle_start as mod_start, handle_delete_message
from handlers.user import handle_start as user_start, handle_help, handle_info
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)

# Загрузка переменных окружения
load_dotenv()

# Токен от BotFather
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

if not TOKEN:
    logging.error("Токен бота не установлен. Проверьте переменные окружения.")
    exit(1)

# Создаем бота
bot = telebot.TeleBot(TOKEN)

# Функция уведомления админа
def notify_admin(bot, message):
    if ADMIN_CHAT_ID:
        bot.send_message(ADMIN_CHAT_ID, message)
    else:
        logging.warning("ADMIN_CHAT_ID не установлен. Невозможно отправить сообщение админу.")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    role = get_user_role(message.from_user.id)
    if role == "admin":
        admin_start(bot, message)
    elif role == "moderator":
        mod_start(bot, message)
    else:
        user_start(bot, message)

# Обработчик команды /help (для всех пользователей)
@bot.message_handler(commands=['help'])
def help_command(message):
    handle_help(bot, message)

# Обработчик команды /info (для всех пользователей)
@bot.message_handler(commands=['info'])
def info_command(message):
    handle_info(bot, message)

# Команда для добавления модератора (только админ)
@bot.message_handler(commands=['add_moderator'])
def add_moderator_command(message):
    role = get_user_role(message.from_user.id)
    if role == 'admin':
        handle_add_moderator(bot, message)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

# Команда для удаления пользователя (только админ)
@bot.message_handler(commands=['remove_user'])
def remove_user_command(message):
    role = get_user_role(message.from_user.id)
    if role == 'admin':
        handle_remove_user(bot, message)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

# Команда для удаления сообщений (только модератор)
@bot.message_handler(commands=['delete_message'])
def delete_message_command(message):
    role = get_user_role(message.from_user.id)
    if role == 'moderator':
        handle_delete_message(bot, message)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

# Запуск бота
try:
    logging.info("Бот запущен.")
    bot.polling(none_stop=True)
except Exception as e:
    logging.error(f"Ошибка в бот-поллинге: {e}")
    notify_admin(bot, f"Критическая ошибка: {e}")
