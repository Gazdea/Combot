from telegram.ext import Application
import os
import logging

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logging.error("Токен бота не установлен. Проверьте переменные окружения.")
    exit(1)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

application = Application.builder().token(TOKEN).build()