from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, CommandHandler
import logging
from app.di import HandlerContainer
from app.config import application
from app.bot.middlewares import global_error_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
logger = logging.getLogger(__name__)
    
# ===============================
# Обработчики команд
# ===============================

handler_container = HandlerContainer

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command_handler = handler_container.command_handler()
    await command_handler.get_method_from_command(update, context)

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command_handler = handler_container.command_handler()
    await command_handler.welcome_new_member(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command_handler = handler_container.command_handler()
    member = await context.bot.get_chat_member(chat_id=update.message.chat_id, user_id=update.message.from_user.id)
    await command_handler.save_message(update, context)
    if member.status not in ['administrator', 'creator']:
        await command_handler.remove_links(update, context)
        await command_handler.anti_spam_protection(update, context)

#TODO DEBUGGER
async def handle_debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    debug_handler = handler_container.debug_handler()
    await debug_handler.debug(update, context)
    
# ===============================
# Запуск бота
# ===============================

def run_bot():
    # Регистрация обработчиков
    application.add_handler(CommandHandler("debug", handle_debug))
    application.add_handler(MessageHandler(filters.COMMAND, handle_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.add_error_handler(global_error_handler)    
    # Запуск бота
    application.run_polling()
