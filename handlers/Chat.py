from datetime import datetime, timedelta
import re
from time import sleep
from aiogram import types
from Service import Chat, Command, Message, MutedUser, Role, RolePermission, User, UserChat


class ChatHandlers:
    @staticmethod
    async def anti_spam_protection(message: types.Message):
        """Защита от спама: если пользователь отправляет больше max_messages за time_window секунд, он заглушается."""
        mute_user = MutedUser.get_mute_user(message.from_user.id, message.chat.id)
        if mute_user:
            await message.answer(f"Пользователь замучен до {mute_user.mute_end}")
            await mute_user(message, mute_user.chat_id, mute_user.user_id, mute_user.mute_end)

    @staticmethod
    async def remove_links(message: types.Message):
        """Удаляет сообщения, содержащие ссылки."""
        chat_dto = Chat.get_chat_by_id(message.chat.id)
        if re.search(chat_dto.delete_pattern, message.text):
            await message.bot.delete_message(message.chat.id, message.message_id)

    @staticmethod
    async def welcome_new_member(message: types.Message):
        """Приветствие новых пользователей в чате. Если бот добавлен в чат, добавляет информацию о чате и администраторах."""
        bot_added = False
        for member in message.new_chat_members:
            if member.id == member.bot.id:
                bot_added = True
            else:
                User.add_user(member.id, member.username if member.username else member.first_name)
                UserChat.add_user_by_chat(member.id, message.chat.id, 'user')
                await message.answer(f'Добро пожаловать в наш чат, {member.username if member.username else member.first_name}!')

        if bot_added:
            Chat.new_chat(message.chat.id, message.chat.title)
            admins = await message.bot.get_chat_administrators(message.chat.id)
            for admin in admins:
                User.add_user(admin.user.id, admin.user.username)
                UserChat.add_user_by_chat(admin.user.id, message.chat.id, 'admin')
            await message.answer('Спасибо, что пригласили меня. Теперь я готов работать!')
    
    @staticmethod
    async def save_message(message: types.Message):
        """Сохранение сообщения"""
        Message.save_message(message.message_id ,message.chat.id, message.from_user.id, message.text, message.content_type, message.date.isoformat())
