from db.connection import add_user, log_message

def handle_start(bot, message):
    """Приветствие для обычного пользователя."""
    add_user(message.from_user.id, message.from_user.username, message.chat.id)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!")
    log_message(message.from_user.id, "/start")

def handle_help(bot, message):
    """Вывод справки."""
    help_text = """
    Доступные команды:
    /start - Начать работу с ботом
    /help - Получить справку
    /info - Получить информацию о боте
    """
    bot.send_message(message.chat.id, help_text)

def handle_info(bot, message):
    """Вывод информации о боте."""
    bot_info = """
    Этот бот позволяет управлять пользователями и модерацией чата.
    Разработан для упрощения администрирования.
    """
    bot.send_message(message.chat.id, bot_info)
    log_message(message.from_user.id, "/info")
