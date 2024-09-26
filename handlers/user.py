from handlers.handler import Handler

class user(Handler):
    
    def start(self, bot, message):
        """Приветствие для обычного пользователя."""
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!")

    def help(self, bot, message):
        """Вывод справки."""
        help_text = """
        Доступные команды:
        /start - Начать работу с ботом
        /help - Получить справку
        /info - Получить информацию о боте
        """
        bot.send_message(message.chat.id, help_text)

