from datetime import datetime
from aiogram import types
from .Util import get_mentions, extract_datetime_from_message, mute_user
from Service import Chat, Command, Message, MutedUser, Role, RolePermission, User, UserChat

class CommandHandlers:    
    async def execute_command(self, message: types.Message):
        """Выполняет команду, если она доступна пользователю."""
        command_input = message.text.split()[0].split('@')[0]
        
        available_commands = Command.get_commands_by_chat_user(message.chat.id, message.from_user.id)
        command_match = next((cmd for cmd in available_commands if cmd.command == f'{command_input}'), None)
        if command_match:
            command_method = getattr(self, command_match.command_name, None)
            await command_method(message)
        else:
            await message.answer(f"Команда {command_input} вам не доступна.")

    async def start(self, message: types.Message):
        """Проверка работоспособности бота и подключений."""
        response = ["Запускаю проверку системы..."]

        # Проверка подключения к API Telegram
        try:
            bot_info = await message.bot.get_me()
            response.append(f"Подключение к API Telegram успешно.\nИмя бота: {bot_info.first_name}\nUsername: @{bot_info.username}")
        except Exception as e:
            response.append(f"Ошибка подключения к API Telegram: {str(e)}")
            await message.answer("\n".join(response))
            return

        # Проверка административных прав бота в чате
        try:
            chat_member = await message.bot.get_chat_member(message.chat.id, message.bot.id)
            if isinstance(chat_member, (types.ChatMemberAdministrator, types.ChatMemberOwner)):
                response.append("У бота есть административные права в этом чате.")
            else:
                response.append("У бота нет административных прав в этом чате.")
        except Exception as e:
            response.append(f"Ошибка проверки прав администратора: {str(e)}")

        # Проверка подключения к базе данных
        try:
            chat_info = Chat.get_chat_by_id(message.chat.id)
            if chat_info:
                response.append("Подключение к базе данных успешно. Чат найден в базе данных.")
            else:
                response.append("Чат не найден в базе данных. Создаю запись.")
                Chat.new_chat(message.chat.id, message.chat.title)
        except Exception as e:
            response.append(f"Ошибка подключения к базе данных: {str(e)}")

        # Проверка: является ли сообщение ответом на другое сообщение
        if message.reply_to_message:
            response.append("Это сообщение является ответом на другое сообщение.")
        else:
            response.append("Нет ответа на сообщение.")

        # Получение упомянутых пользователей, кроме бота
        users = await get_mentions(message)
        if users:
            response.append(f"Упомянутые пользователи (кроме бота): {', '.join([user.username for user in users])}")
        else:
            response.append("Нет упомянутых пользователей (кроме бота).")

        # Извлечение даты и времени из сообщения
        extracted_date = await extract_datetime_from_message(message)
        if extracted_date:
            response.append(f"Извлечённая дата и время: {extracted_date.strftime('%d.%m.%Y %H:%M')}")
        else:
            response.append("Дата и время не указаны или не распознаны.")

        # Отправка собранного сообщения
        response.append("Проверка завершена успешно.")
        await message.answer("\n".join(response))

    async def info(self, message: types.Message):
        """Вывод информации о боте для админа."""
        bot_info = """
    Этот бот позволяет модерировать чат.
    Разработан для упрощения администрирования.
    Создатель @Gazdea
    Репозиторий: https://github.com/Gazdea/Combot
        """
        await message.answer(bot_info)

    async def help(self, message: types.Message):
        """Получить список возможных команд"""
        available_commands = Command.get_commands_by_chat_user(message.chat.id, message.from_user.id)
        if available_commands:
            commands = ""
            for command in available_commands:
                commands += command.command + " " + command.description + "\n"
            await message.answer(commands)

    async def mute(self, message: types.Message):
        """Заглушить пользователя."""
        mentions = await get_mentions(message)
        datetime = await extract_datetime_from_message(message)
        if mentions:
            for mention in mentions:
                await mute_user(message, message.chat.id, mention.user.id, datetime)
                await message.answer(f'Пользователь {mention.user.username} заглушен до {datetime}')

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

    async def delete_message(self, message: types.Message):
        """Удаляет сообщение из чата."""
        if message.reply_to_message:
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        else:
            await message.answer('Необходимо указать, какое сообщение вы хотите удалить.')

    async def chat_spam_mute_time_set(self, message: types.Message):
        chat = Chat.get_chat_by_id(message.chat.id)
        chat.spam_mute_time = message.text.split()[1]
        Chat.save_chat(chat)

    async def chat_spam_num_message_set(self, message: types.Message):
        chat = Chat.get_chat_by_id(message.chat.id)
        chat.spam_message = float[message.text.split()[1]]
        Chat.save_chat(chat)
    
    async def chat_spam_time_set(self, message: types.Message):
        chat = Chat.get_chat_by_id(message.chat.id)
        chat.spam_time = message.text.split()[1]
        Chat.save_chat(chat)
        
    async def chat_delete_pattern_set(self, message: types.Message):
        chat = Chat.get_chat_by_id(message.chat.id)
        chat.delete_pattern = message.text.split()[1]
        Chat.save_chat(chat)
        
    async def role_add(self, message: types.Message):
        """"""
        
    async def role_delete(self, message: types.Message):
        """"""
        
    async def role_command_add(self, message: types.Message):
        """"""
        
    async def role_command_delete(self, message: types.Message):
        """"""
        
    async def role_user_set(self, message: types.Message):
        """"""
        
    async def command_rename(self, message: types.Message):
        """"""
        
    async def chat_user(self, message: types.Message):
        """"""
        
    async def chat_stats_user_join(self, message: types.Message):
        """"""
        
    async def chat_stats_user_active(self, message: types.Message):
        """"""