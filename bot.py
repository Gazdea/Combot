import os
import re
import logging
import threading
from time import time
from collections import defaultdict
from dotenv import load_dotenv
import telebot

# Импорт модулей приложения
from db.connection import add_chat_and_users, get_user_role, add_user
from handlers.admin import Admin
from handlers.moderator import Moderator
from handlers.user import user

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

# Создание бота
bot = telebot.TeleBot(TOKEN)

# Функция уведомления админа
def notify_admin(bot, message):
    if ADMIN_CHAT_ID:
        bot.send_message(ADMIN_CHAT_ID, message)
    else:
        logging.warning("ADMIN_CHAT_ID не установлен. Невозможно отправить сообщение админу.")

# ===============================
# Фабрика обработчиков по ролям
# ===============================
class HandlerFactory:
    @staticmethod
    def get_handler(message):
        """Возвращает обработчик на основе роли пользователя"""
        user_id = message.from_user.id
        role = get_user_role(user_id)
        
        if role == 'admin':
            return Admin()
        elif role == 'moderator':
            return Moderator()
        else:
            return user()

# ===============================
# Обработчики команд
# ===============================
@bot.message_handler(commands=['start'])
def start_command(message):
    handler = HandlerFactory.get_handler(message)
    handler.start(bot, message)

@bot.message_handler(commands=['help'])
def help_command(message):
    handler = HandlerFactory.get_handler(message)
    handler.help(bot, message)

@bot.message_handler(commands=['info'])
def info_command(message):
    handler = HandlerFactory.get_handler(message)
    handler.info(bot, message)

@bot.message_handler(commands=['add_moderator'])
def add_moderator_command(message):
    handler = HandlerFactory.get_handler(message)
    handler.add_moderator(bot, message)

@bot.message_handler(commands=['remove_user'])
def remove_user_command(message):
    handler = HandlerFactory.get_handler(message)
    handler.remove_user(bot, message)

@bot.message_handler(commands=['delete_message'])
def delete_message_command(message):
    handler = HandlerFactory.get_handler(message)
    handler.delete_message(bot, message)

# ===============================
# Приветственные сообщения
# ===============================
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    if not message.new_chat_members:
        logging.warning("new_chat_members is None or empty")
        return
    
    for new_user in message.new_chat_members:
        if new_user.id == bot.get_me().id:
            chat_id = message.chat.id
            bot.send_message(chat_id, "Бот добавлен в этот чат! Привет!")
            members = bot.get_chat_administrators(chat_id)
            add_chat_and_users(chat_id, [member.user for member in members])
            logging.info(f"Бот добавлен в чат {chat_id}, пользователи добавлены в БД.")
        else:
            add_user(new_user, message.chat.id)
            welcome_text = f"Привет, {new_user.first_name}! Добро пожаловать в наш чат."
            bot.send_message(message.chat.id, welcome_text)

# ===============================
# Защита от спама
# ===============================
spams = {}
msgs = 4  # Количество сообщений
max_time = 5  # Время в секундах
ban_time = 300  # Время бана в секундах

def is_spam(user_id):
    current_time = int(time())
    
    if user_id in spams:
        usr = spams[user_id]
        if usr["banned"] > current_time:
            logging.info(f"Пользователь {user_id} забанен.")
            return True
        
        if usr["next_time"] > current_time:
            usr["messages"] += 1
            if usr["messages"] >= msgs:
                usr["banned"] = current_time + ban_time
                logging.info(f"Пользователь {user_id} забанен за спам.")
                return True
        else:
            usr["messages"] = 1
            usr["next_time"] = current_time + max_time
    else:
        spams[user_id] = {"next_time": current_time + max_time, "messages": 1, "banned": 0}
    
    return False

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if is_spam(user_id):
        bot.send_message(message.chat.id, "Вы забанены за спам. Пожалуйста, подождите перед отправкой сообщений.")

# ===============================
# Запуск бота
# ===============================
try:
    logging.info("Бот запущен.")
    bot.infinity_polling()
except Exception as e:
    logging.error(f"Ошибка в бот-поллинге: {e}")
    notify_admin(bot, f"Критическая ошибка: {e}")
