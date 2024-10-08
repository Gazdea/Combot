from handlers.handler import Handler, delete_message, kick, mute, unmute
from aiogram import types

class Moderator(Handler):
    
    async def start(self, message: types.Message):
        """Приветствие для модератора."""
        await message.answer("Привет, модератор! Чем могу помочь?")
        
    async def help(self, message: types.Message):
        """Вывод справки."""
        help_text = """
        Доступные команды:
        /start - Начать работу с ботом
        /help - Получить справку
        /info - Получить информацию о боте
        /delete - Удалить сообщение (ответьте на сообщение, которое хотите удалить)
        /mute - Заглушить пользователя (ответьте на сообщение пользователя)
        /unmute - Снять заглушение с пользователя (ответьте на сообщение пользователя)
        /kick - Выгнать пользователя
        """
        await message.answer(help_text)

    async def delete_message(self, message: types.Message):
        """Удаление сообщения."""
        await delete_message(message)

    async def mute(self, message: types.Message):
        """Заглушить пользователя."""
        await mute(message)

    async def unmute(self, message: types.Message):
        """Снять мут с пользователя."""
        await unmute(message)

    async def kick(self, message: types.Message):
        """Выгнать пользователя"""
        await kick(message)