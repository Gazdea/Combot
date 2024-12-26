import logging
from app.config import application, get_url
from app.bot import  handler
from app.bot.middlewares import global_error_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# ===============================
# Запуск бота
# ===============================

def __main__():
    # Регистрация обработчиков
    application.add_error_handler(global_error_handler)
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    __main__()