import re
from app.db.model.DTO import MessageDTO, UserDTO
from app.bot.handler.CommandHandler import CommandHandler
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from app.db.service import CommandDBService, MutedUserDBService, UserDBService, ChatDBService, UserChatDBService, MessageDBService

class CommandHandlerImpl(CommandHandler):
    def __init__(self, command_service: CommandDBService, muted_user_service: MutedUserDBService, user_service: UserDBService, chat_service: ChatDBService, user_chat_service: UserChatDBService, message_service: MessageDBService):
        self.command_service = command_service
        self.muted_user_service = muted_user_service
        self.user_service = user_service
        self.chat_service = chat_service
        self.user_chat_service = user_chat_service
        self.message_service = message_service
    
    async def get_method_from_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команд с делегированием в соответствующие методы"""
        message = update.message
        command_input = message.text.split()[0].split('@')[0]
        command_method = self._get_command_method(command_input)
        if command_method:
            try:
                await command_method(update, context)
            except Exception as e:
                await message.reply_text(f"Ошибка выполнения команды: {str(e)}")
        else:
            await message.reply_text(f"Команда {command_input} вам не доступна.")

    def _get_command_method(self, command_input: str, chat_id: int, user_id: int):
        """Находит метод, который нужно вызвать для команды"""
        available_command = self.command_service.get_command_by_chat_user_name(chat_id, user_id, command_input)
        return getattr(self, available_command.method_name, None)

  
    async def anti_spam_protection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Защита от спама: если пользователь отправляет больше max_messages за time_window секунд, он заглушается."""
        message = update.message
        if mute_user := self.muted_user_service.get_mute_user(
            message.chat.id, message.from_user.id
        ):
            await context.bot.restrict_chat_member(
                chat_id=mute_user.chat_id,
                user_id=mute_user.user_id,
                permissions=ChatPermissions.no_permissions(),
                until_date=mute_user.time_end
            )


    async def remove_links(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удаляет сообщения, содержащие ссылки."""
        message = update.message
        chat_dto = self.chat_service.get_chat_by_id(message.chat.id)
        
        if re.search(chat_dto.delete_pattern, message.text):
            await context.bot.delete_message(message.chat.id, message.message_id)


    async def welcome_new_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Приветствие новых пользователей в чате. Если бот добавлен в чат, добавляет информацию о чате и администраторах."""
        message = update.message
        bot_added = False
        
        for member in message.new_chat_members:
            if member.id == context.bot.id:
                bot_added = True
            else:
                self.user_service.add_user(UserDTO(id=member.id, username=member.username))
                self.user_chat_service.add_user_by_chat(member.id, message.chat.id, 'user', message.date)
                await context.bot.send_message(message.chat.id, f'Добро пожаловать в наш чат, {member.username or member.first_name}!')

        if bot_added:
            self.chat_service.new_chat(message.chat.id, message.chat.title)
            admins = await context.bot.get_chat_administrators(message.chat.id)
            for admin in admins:
                self.user_service.add_user(UserDTO(id=admin.user.id, username=admin.user.username))
                self.user_chat_service.add_user_by_chat(admin.user.id, message.chat.id, 'admin', message.date)
            await context.bot.send_message(message.chat.id, 'Спасибо, что пригласили меня. Теперь я готов работать!')
            await context.bot.send_message(message.chat.id, 'Для корректной работы с чатом не забудьте установить права администратора.')


    async def save_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Сохранение сообщения"""
        message = update.message
        user = self.user_service.get_user_by_id(message.from_user.id)
        if user.is_error():
            await update.message.reply_text("Кто ты воин, дай как запишу тебя")
            self.user_service.add_user(UserDTO(id=message.from_user.id, username=message.from_user.username))
        user_chat = self.user_chat_service.get_user_chat(message.chat.id, message.from_user.id)
        if not user_chat:
            self.user_chat_service.add_user_by_chat(message.from_user.id, message.chat.id, 'user', message.date)
            
        self.message_service.save_message(
            MessageDTO(
                message_id=message.message_id,
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                message=message.text,
                date=message.date
            )
        )
