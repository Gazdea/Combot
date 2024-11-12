from telegram.ext import Application
import os
import logging

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logging.error("Токен бота не установлен. Проверьте переменные окружения.")
    exit(1)

application = Application.builder().token(TOKEN).build()