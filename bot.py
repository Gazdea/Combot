from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, CommandHandler
import logging
from handlers import execute_command, welcome_new_member, save_message, remove_links, anti_spam_protection
from config import application
from handlers import debug

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
logger = logging.getLogger(__name__)
    
# ===============================
# Обработчики команд
# ===============================

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await execute_command(update, context)

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await welcome_new_member(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(chat_id=update.message.chat_id, user_id=update.message.from_user.id)
    await save_message(update, context)
    if member.status not in ['administrator', 'creator']:
        await remove_links(update, context)
        await anti_spam_protection(update, context)

#TODO DEBUGGER
async def handle_debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await debug.debug(update, context)
    
# ===============================
# Запуск бота
# ===============================

def main():
    # Регистрация обработчиков
    application.add_handler(CommandHandler("debug", handle_debug))
    application.add_handler(MessageHandler(filters.COMMAND, handle_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Запуск бота
    application.run_polling()
    logger.info("Бот запущен.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Ошибка в бот-поллинге: {e}")
