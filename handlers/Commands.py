from datetime import datetime
import random
from telegram import Update
from telegram.ext import ContextTypes
from .Util import get_mentioned_users, extract_datetime_from_message, muted_user
from service import ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermisionService
from resourse.bot_response import start_responses, bot_info

class CommandHandlers:
    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Выполняет команду, если она доступна пользователю."""
        message = update.message
        command_input = message.text.split()[0].split('@')[0]

        available_commands = CommandService().get_commands_by_chat_user(message.chat.id, message.from_user.id)
        command_match = next((cmd for cmd in available_commands if cmd.command == f'{command_input}'), None)

        if command_match:
            command_method = getattr(self, command_match.command_name, None)
            if command_method:
                await command_method(update, context)
        else:
            await message.reply_text(f"Команда {command_input} вам не доступна.")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Потешный старт"""
        response = random.choice(start_responses)
        await update.message.reply_text(response.format(username=update.message.from_user.username))
        
    async def info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вывод информации о боте для админа."""
        await update.message.reply_text(bot_info)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить список возможных команд"""
        message = update.message
        available_commands = CommandService().get_commands_by_chat_user(message.chat.id, message.from_user.id)
        if available_commands:
            commands = "\n".join([f"{cmd.command} - {cmd.description}" for cmd in available_commands])
            await message.reply_text(commands)

    async def mute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Заглушить пользователя."""
        message = update.message
        users = await get_mentioned_users(update, context)
        mute_until = await extract_datetime_from_message(update, context)
        if users:
            for user in users:
                await muted_user(update, context, message.chat.id, user.id, mute_until)
                await message.reply_text(f'Пользователь {user.username} заглушен до {mute_until}')

    async def unmute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Снять мут с пользователя."""
        message = update.message
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention' and entity.user:
                    try:
                        await context.bot.restrict_chat_member(
                            chat_id=message.chat.id,
                            user_id=entity.user.id,
                            until_date=datetime.now()
                        )
                        await message.reply_text(f'Мут с пользователя {entity.user.username} снят.')
                    except Exception as e:
                        await message.reply_text(f'Не удалось снять мут с пользователя: {e}')
                    return
        await message.reply_text('Необходимо указать пользователя, с которого нужно снять мут.')

    async def kick(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Выгнать пользователя из чата."""
        message = update.message
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention' and entity.user:
                    try:
                        await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=entity.user.id)
                        await message.reply_text(f'Пользователь {entity.user.username} выгнан из чата.')
                    except Exception as e:
                        await message.reply_text(f'Не удалось выгнать пользователя: {e}')
                    return
        await message.reply_text('Необходимо указать пользователя, которого нужно выгнать.')

    async def ban(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Забанить пользователя."""
        message = update.message
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention' and entity.user:
                    try:
                        await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=entity.user.id)
                        await message.reply_text(f'Пользователь {entity.user.username} забанен.')
                    except Exception as e:
                        await message.reply_text(f'Не удалось забанить пользователя: {e}')
                    return
        await message.reply_text('Необходимо указать пользователя, которого нужно забанить.')

    async def unban(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Разбанить пользователя."""
        message = update.message
        if message.entities:
            for entity in message.entities:
                if entity.type == 'mention' and entity.user:
                    try:
                        await context.bot.unban_chat_member(chat_id=message.chat.id, user_id=entity.user.id)
                        await message.reply_text(f'Пользователь {entity.user.username} разбанен.')
                    except Exception as e:
                        await message.reply_text(f'Не удалось разбанить пользователя: {e}')
                    return
        await message.reply_text('Необходимо указать пользователя, которого нужно разбанить.')

    async def delete_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удаляет сообщение из чата."""
        message = update.message
        if message.reply_to_message:
            await context.bot.delete_message(message.chat.id, message.message_id)
            await context.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        else:
            await message.reply_text('Необходимо указать, какое сообщение вы хотите удалить.')

    async def chat_spam_mute_time_set(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Устанавливает время мьюта за спам для чата."""
        message = update.message
        chat = ChatService().get_chat_by_id(message.chat.id)
        chat.spam_mute_time = int(message.text.split()[1])
        ChatService().save_chat(chat)
        await message.reply_text("Время мьюта за спам установлено.")

    async def chat_spam_num_message_set(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Устанавливает количество сообщений для срабатывания антиспам защиты."""
        message = update.message
        chat = ChatService().get_chat_by_id(message.chat.id)
        chat.spam_message = int(message.text.split()[1])
        ChatService().save_chat(chat)
        await message.reply_text("Число сообщений для антиспам установлено.")

    async def chat_spam_time_set(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Устанавливает время, в течение которого считается количество сообщений для антиспам защиты."""
        message = update.message
        chat = ChatService().get_chat_by_id(message.chat.id)
        chat.spam_time = int(message.text.split()[1])
        ChatService().save_chat(chat)
        await message.reply_text("Время антиспам защиты установлено.")

    async def chat_delete_pattern_set(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Устанавливает шаблон для автоматического удаления сообщений."""
        message = update.message
        chat = ChatService().get_chat_by_id(message.chat.id)
        chat.delete_pattern = message.text.split()[1]
        ChatService().save_chat(chat)
        await message.reply_text("Шаблон удаления сообщений установлен.")

    async def role_add(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Добавляет новую роль в чат."""
        message = update.message
        await message.reply_text("Роль добавлена.")

    async def role_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удаляет роль из чата."""
        message = update.message
        await message.reply_text("Роль удалена.")

    async def role_command_add(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Добавляет команду в указанную роль."""
        message = update.message
        await message.reply_text("Команда добавлена к роли.")

    async def role_command_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удаляет команду из указанной роли."""
        message = update.message
        await message.reply_text("Команда удалена из роли.")

    async def role_user_set(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Назначает роль пользователю."""
        message = update.message
        await message.reply_text("Роль назначена пользователю.")

    async def command_rename(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Переименовывает команду."""
        message = update.message
        await message.reply_text("Команда переименована.")

    async def chat_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получает информацию о пользователе в чате."""
        message = update.message
        await message.reply_text("Информация о пользователе в чате.")

    async def chat_stats_user_join(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отображает статистику присоединения пользователя к чату."""
        message = update.message
        await message.reply_text("Статистика присоединения пользователя.")

    async def chat_stats_user_active(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отображает статистику активности пользователя в чате."""
        message = update.message
        await message.reply_text("Статистика активности пользователя.")