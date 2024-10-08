from handlers.handler import Handler, ban, delete_message, kick, mute, unban, unmute  # Импортируем базовый класс Handler
from aiogram import types

class Admin(Handler):
    def __init__(self):
        super().__init__()
    
    async def start(self, message: types.Message):
        """Приветствие для админа."""
        await message.answer("Привет, админ! Что хотите сделать?")
        
    async def help(self, message: types.Message):
        """Вывод справки по доступным командам для админа."""
        help_text = """
        Доступные команды:
        /start - Начать работу с ботом
        /help - Получить справку
        /info - Получить информацию о боте
        /kick - Выгнать пользователя (ответом на сообщение или через упоминание)
        /mute - Заглушить пользователя (ответом на сообщение или через упоминание)
        /unmute - Снять заглушение с пользователя (ответом на сообщение или через упоминание)
        /ban - Забанить пользователя (ответом на сообщение или через упоминание)
        /unban - Разбанить пользователя (ответом на сообщение или через упоминание)
        /delete - Удалить сообщение (доступно также для модераторов)
        """
        await message.answer(help_text)

    async def delete_message(self, message: types.Message):
        """Удалить сообщение."""
        await delete_message(message)

    async def kick(self, message: types.Message):
        """Выгнать пользователя."""
        await kick(message)

    async def mute(self, message: types.Message):
        """Заглушить пользователя."""
        await mute(message)

    async def unmute(self, message: types.Message):
        """Снять мут с пользователя."""
        await unmute(message)

    async def ban(self, message: types.Message):
        """Забанить пользователя."""
        await ban(message)

    async def unban(self, message: types.Message):
        """Разбанить пользователя."""
        await unban(message)
