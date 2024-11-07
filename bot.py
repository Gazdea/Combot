import os
import logging
import asyncio
from telethon import Bot, Dispatcher, types

# Импорт модулей приложения
from handlers import CommandHandlers, ChatHandlers

# Получение токена и ID админа
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

if not TOKEN:
    logging.error("Токен бота не установлен. Проверьте переменные окружения.")
    exit(1)

# Создание объектов бота и диспетчера
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)

# ===============================
# Обработчики команд
# ===============================

@dp.message_handler(lambda message: message.text.startswith('/'))
async def handle_command(message: types.Message):
    await CommandHandlers().execute_command(message)

@dp.message_handler(content_types=['new_chat_members'])
async def new_member(message: types.Message):
    await ChatHandlers().welcome_new_member(message)

@dp.message_handler()
async def handle_message(message: types.Message):
    member = await message.chat.get_member(message.from_user.id)
    if not member.is_chat_admin():
        await ChatHandlers().save_message(message)
        await ChatHandlers().remove_links(message)
        await ChatHandlers().anti_spam_protection(message)
# ===============================
# Запуск бота
# ===============================

if __name__ == "__main__":
    try:
        asyncio.run(dp.start_polling())
        logging.info("Бот запущен.")
    except Exception as e:
        logging.error(f"Ошибка в бот-поллинге: {e}")
