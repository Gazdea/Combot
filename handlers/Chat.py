from datetime import datetime, timedelta
import re
from telegram import Update
from telegram.ext import ContextTypes
from models.DTO import MessageDTO, UserDTO
from service import ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermisionService
from .Util import muted_user
class ChatHandlers:
    @staticmethod
    async def anti_spam_protection(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Защита от спама: если пользователь отправляет больше max_messages за time_window секунд, он заглушается."""
        message = update.message
        mute_user = MutedUserService().get_mute_user(message.chat.id, message.from_user.id)
        if mute_user:
            await muted_user(update, context, mute_user)

    @staticmethod
    async def remove_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удаляет сообщения, содержащие ссылки."""
        message = update.message
        chat_dto = ChatService().get_chat_by_id(message.chat.id)
        
        if re.search(chat_dto.delete_pattern, message.text):
            await context.bot.delete_message(message.chat.id, message.message_id)

    @staticmethod
    async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Приветствие новых пользователей в чате. Если бот добавлен в чат, добавляет информацию о чате и администраторах."""
        message = update.message
        bot_added = False
        
        for member in message.new_chat_members:
            if member.id == context.bot.id:
                bot_added = True
            else:
                UserService().add_user(UserDTO(id=member.id, username=member.username))
                UserChatService().add_user_by_chat(member.id, message.chat.id, 'user')
                await update.message.reply_text(f'Добро пожаловать в наш чат, {member.username if member.username else member.first_name}!')

        if bot_added:
            ChatService().new_chat(message.chat.id, message.chat.title)
            admins = await context.bot.get_chat_administrators(message.chat.id)
            for admin in admins:
                UserService().add_user(UserDTO(admin.user.id, admin.user.username))
                UserChatService().add_user_by_chat(admin.user.id, message.chat.id, 'admin')
            await message.reply_text('Спасибо, что пригласили меня. Теперь я готов работать!')

    @staticmethod
    async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Сохранение сообщения"""
        message = update.message
        MessageService().save_message(
            MessageDTO(
                message_id=message.message_id,
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                message=message.text,
                date=message.date.isoformat()
            )
        )
