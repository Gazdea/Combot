from handlers.handler import Handler
from aiogram import types

class User(Handler):  # Измените название класса на 'User' для соблюдения PEP 8
    async def start(self, message: types.Message):
        """Приветствие для обычного пользователя."""
        await message.answer(f"Привет, {message.from_user.first_name}!")

    async def help(self, message: types.Message):
        """Вывод справки."""
        help_text = """
        Доступные команды:
        /start - Начать работу с ботом
        /help - Получить справку
        /info - Получить информацию о боте
        """
        await message.answer(help_text)