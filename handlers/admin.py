from db.connection import add_user, remove_user
from handlers.handler import Handler  # Если handler — это класс, его нужно правильно импортировать
from handlers.moderator import Moderator  # Если moderator — это класс

class Admin(Handler):
    def __init__(self):
        super().__init__()
        self.moderator = Moderator()  # Создаем объект модератора
    
    def start(self, bot, message):
        """Приветствие для админа."""
        bot.send_message(message.chat.id, "Привет, админ! Что хотите сделать?")
        
    def help(self, bot, message):
        """Вывод справки по доступным командам для админа."""
        help_text = """
        Доступные команды:
        /start - Начать работу с ботом
        /help - Получить справку
        /info - Получить информацию о боте
        /add_moderator - Добавить модератора по ID
        /remove_user - Удаление пользователя по ID
        /delete_message - Удалить сообщение (доступно также для модераторов)
        """
        bot.send_message(message.chat.id, help_text)

    def delete_message(self, bot, message):
        """Администратор может использовать метод модератора для удаления сообщения."""
        self.moderator.delete_message(bot, message)
    
    @staticmethod
    def add_moderator(bot, message):
        """Добавление модератора по ID пользователя."""
        try:
            # Ожидается команда в формате /add_moderator <user_id>
            user_id = int(message.text.split()[1])
            add_user(user_id, username=None, chat_id=None, role_name="moderator")
            bot.send_message(message.chat.id, f"Пользователь {user_id} теперь модератор.")
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, "Используйте правильный формат команды: /add_moderator <user_id>")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

    @staticmethod
    def remove_user(bot, message):
        """Удаление пользователя по ID."""
        try:
            # Ожидается команда в формате /remove_user <user_id>
            user_id = int(message.text.split()[1])
            if remove_user(user_id):
                bot.send_message(message.chat.id, f"Пользователь {user_id} удален.")
            else:
                bot.send_message(message.chat.id, f"Пользователь {user_id} не найден.")
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, "Используйте правильный формат команды: /remove_user <user_id>")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
