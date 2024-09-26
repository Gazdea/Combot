from db.connection import log_message
from handlers.handler import Handler

class Moderator(Handler):
    
    def start(self, bot, message):
        """Приветствие для модератора."""
        bot.send_message(message.chat.id, "Привет, модератор! Чем могу помочь?")
        
    def help(self, bot, message):
        """Вывод справки."""
        help_text = """
        Доступные команды:
        /start - Начать работу с ботом
        /help - Получить справку
        /info - Получить информацию о боте
        /delete_message - Удалить сообщение по ID
        """
        bot.send_message(message.chat.id, help_text)

    @staticmethod
    def delete_message(bot, message):
        """Удаление сообщения по ID (только модератор)."""
        try:
            message_id = int(message.text.split()[1])  # Ожидается, что модератор введет команду в формате /delete_message <message_id>
            bot.delete_message(message.chat.id, message_id)
            bot.send_message(message.chat.id, f"Сообщение {message_id} удалено.")
            log_message(message.from_user.id, f"Deleted message {message_id}", message_type="moderation")
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, "Используйте правильный формат команды: /delete_message <message_id>")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка при удалении сообщения: {e}")
    
    @staticmethod
    def add_user(bot, message):
        """
        """
