from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def start(self, bot, message):
        pass
    
    @abstractmethod
    def help(self, bot, message):
        pass
    
    # @abstractmethod
    def info(self, bot, message):
        """Вывод информации о боте для админа."""
        bot_info = """
        Этот бот позволяет управлять пользователями и модерацией чата.
        Разработан для упрощения администрирования.
        Создатель @Gazdea
        """
        bot.send_message(message.chat.id, bot_info)
        pass

