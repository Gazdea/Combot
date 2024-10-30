from datetime import datetime, timedelta
import re
from time import sleep
from aiogram import types
from Service.Service import ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermissionService

class Handlers:    
    async def execute_command(self, message: types.Message):
        """Выполняет команду, если она доступна пользователю."""
        command_input = message.text.split()[0]
        available_commands = CommandService().get_commands_by_chat_user(message.chat.id, message.from_user.id)
        command_match = next((cmd for cmd in available_commands if cmd.command == f'{command_input}'), None)
        if command_match:
            command_method = getattr(self, command_match.command_name, None)
            await command_method(message)
        else:
            await message.answer(f"Команда {command_input} вам не доступна.")

    async def info(self, message: types.Message):
        """Вывод информации о боте для админа."""
        bot_info = """
    Этот бот позволяет модерировать чат.
    Разработан для упрощения администрирования.
    Создатель @Gazdea
    Репозиторий: https://github.com/Gazdea/Combot
        """
        await message.answer(bot_info)

    async def start(self, message: types.Message):
        """Проверка работоспособности бота и подключений."""
        await message.answer("Запускаю проверку системы...")

        try:
            bot_info = await message.bot.get_me()
            await message.answer(f"Подключение к API Telegram успешно.\nИмя бота: {bot_info.first_name}\nUsername: @{bot_info.username}")
        except Exception as e:
            await message.answer(f"Ошибка подключения к API Telegram: {str(e)}")
            return

        try:
            chat_member = await message.bot.get_chat_member(message.chat.id, message.bot.id)
            if isinstance(chat_member, (types.ChatMemberAdministrator, types.ChatMemberOwner)):
                await message.answer("У бота есть административные права в этом чате.")
            else:
                await message.answer("У бота нет административных прав в этом чате.")
        except Exception as e:
            await message.answer(f"Ошибка проверки прав администратора: {str(e)}")

        try:
            chat_info = ChatService().get_chat_by_id(message.chat.id)
            if chat_info:
                await message.answer("Подключение к базе данных успешно. Чат найден в базе данных.")
            else:
                await message.answer("Чат не найден в базе данных. Создаю запись.")
                ChatService().new_chat(message.chat.id, message.chat.title)
        except Exception as e:
            await message.answer(f"Ошибка подключения к базе данных: {str(e)}")
        await message.answer("Проверка завершена успешно.")

    async def help(self, message: types.Message):
        """Получить список возможных команд"""
        available_commands = CommandService().get_commands_by_chat_user(message.chat.id, message.from_user.id)
        if available_commands:
            commands = ""
            for command in available_commands:
                commands += command.command_name + " " + command.description + "\n"
            await message.answer(commands)
    
    async def delete_message(self, message: types.Message):
        """Удаляет сообщение из чата."""
        if message.reply_to_message:
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        else:
            await message.answer('Необходимо указать, какое сообщение вы хотите удалить.')

    async def kick(self, message: types.Message):
        """Выгнать пользователя из чата."""
        await message.answer(message.entities)
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention' and entity.user:
                    try:
                        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=entity.user.id)
                        await message.answer(f'Пользователь {entity.user.username} выгнан из чата.')
                    except Exception as e:
                        await message.answer(f'Не удалось выгнать пользователя: {e}')
                    return
        await message.answer('Необходимо указать пользователя, которого нужно выгнать.')

    async def mute(self, message: types.Message):
        """Заглушить пользователя."""
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention' and entity.user:
                    try:
                        await self.mute_user(message, message.chat.id, entity.user.id, datetime(message.text))
                        await message.answer(f'Пользователь {entity.user.username} заглушен на 1 минуту.')
                    except Exception as e:
                        await message.answer(f'Не удалось заглушить пользователя: {e}')
                    return
        await message.answer('Необходимо указать пользователя, которого нужно заглушить.')

    async def unmute(self, message: types.Message):
        """Снять мут с пользователя."""
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention' and entity.user:
                    try:
                        await message.bot.restrict_chat_member(
                            chat_id=message.chat.id,
                            user_id=entity.user.id,
                            until_date=datetime.now()
                        )
                        await message.answer(f'Мут с пользователя {entity.user.username} снят.')
                    except Exception as e:
                        await message.answer(f'Не удалось снять мут с пользователя: {e}')
                    return
        await message.answer('Необходимо указать пользователя, с которого нужно снять мут.')

    async def ban(self, message: types.Message):
        """Забанить пользователя."""
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention' and entity.user:
                    try:
                        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=entity.user.id)
                        await message.answer(f'Пользователь {entity.user.username} забанен.')
                    except Exception as e:
                        await message.answer(f'Не удалось забанить пользователя: {e}')
                    return
        await message.answer('Необходимо указать пользователя, которого нужно забанить.')

    async def unban(self, message: types.Message):
        """Разбанить пользователя."""
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention' and entity.user:
                    try:
                        await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=entity.user.id)
                        await message.answer(f'Пользователь {entity.user.username} разбанен.')
                    except Exception as e:
                        await message.answer(f'Не удалось разбанить пользователя: {e}')
                    return
        await message.answer('Необходимо указать пользователя, которого нужно разбанить.')

    async def chat_spam_mute_time_set(self, message: types.Message):
        chat = ChatService().get_chat_by_id(message.chat.id)
        chat.spam_mute_time = message.text.split()[1]
        ChatService().save_chat(chat)

    async def chat_spam_mum_message_set(self, message: types.Message):
        chat = ChatService().get_chat_by_id(message.chat.id)
        chat.spam_message = message.text.split()[1]
        ChatService().save_chat(chat)
    
    async def chat_spam_time_set(self, message: types.Message):
        chat = ChatService().get_chat_by_id(message.chat.id)
        chat.spam_time = message.text.split()[1]
        ChatService().save_chat(chat)
        
    async def chat_delete_pattern_set(self, message: types.Message):
        chat = ChatService().get_chat_by_id(message.chat.id)
        chat.delete_pattern = message.text.split()[1]
        ChatService().save_chat(chat)
        
    async def role_add(self, message: types.Message):
        """"""
    
    @staticmethod
    async def anti_spam_protection(self, message: types.Message):
        """Защита от спама: если пользователь отправляет больше max_messages за time_window секунд, он заглушается."""
        mute_user = MutedUserService().get_mute_user(message.from_user.id, message.chat.id)
        if mute_user:
            await message.answer(f"Пользователь замучен до {mute_user.mute_end}")
            await mute_user(message, mute_user.chat_id, mute_user.user_id, mute_user.mute_end)

    @staticmethod
    async def remove_links(self, message: types.Message):
        """Удаляет сообщения, содержащие ссылки."""
        chat_dto = ChatService().get_chat_by_id(message.chat.id)
        if re.search(chat_dto.delete_pattern, message.text):
            await message.bot.delete_message(message.chat.id, message.message_id)

    @staticmethod
    async def welcome_new_member(self, message: types.Message):
        """Приветствие новых пользователей в чате. Если бот добавлен в чат, добавляет информацию о чате и администраторах."""
        bot_added = False
        for member in message.new_chat_members:
            if member.id == member.bot.id:
                bot_added = True
            else:
                UserService().add_user(member.id, member.username if member.username else member.first_name)
                UserChatService().add_user_by_chat(member.id, message.chat.id, 'user')
                await message.answer(f'Добро пожаловать в наш чат, {member.username if member.username else member.first_name}!')

        if bot_added:
            ChatService().new_chat(message.chat.id, message.chat.title)
            admins = await message.bot.get_chat_administrators(message.chat.id)
            for admin in admins:
                UserService().add_user(admin.user.id, admin.user.username)
                UserChatService().add_user_by_chat(admin.user.id, message.chat.id, 'admin')
            await message.answer('Спасибо, что пригласили меня. Теперь я готов работать!')
    
    @staticmethod
    async def save_message(self, message: types.Message):
        """Сохранение сообщения"""
        MessageService().save_message(message.message_id ,message.chat.id, message.from_user.id, message.text, message.content_type, message.date.isoformat())
    
    @staticmethod
    async def mute_user(self, message: types.Message, chat_id, user_id, mute_end: datetime | timedelta):
        """Выдача мута"""
        await message.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False),
            until_date=mute_end
        )
        await sleep(mute_end)
        await message.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=types.ChatPermissions(can_send_messages=True, can_send_media_messages=True)
        )
        