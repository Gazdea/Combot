from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, CommandHandler

# Импорт модулей приложения
from handlers import CommandHandlers, ChatHandlers, debug
from config import application, logger

# ===============================
# Обработчики команд
# ===============================

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await CommandHandlers().execute_command(update, context)

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ChatHandlers().welcome_new_member(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    member = await context.bot.get_chat_member(chat_id=message.chat_id, user_id=message.from_user.id)
    await ChatHandlers().save_message(update, context)
    if not member.status in ['administrator', 'creator']:
        await ChatHandlers().remove_links(update, context)
        await ChatHandlers().anti_spam_protection(update, context)

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
