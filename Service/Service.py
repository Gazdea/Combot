from datetime import date
from typing import Optional
from aiogram import types
from sqlalchemy import true

from DTO import DTO
from Repository.Repository import ChatRepository, CommandRepository, MessageRepository, RoleRepository, UserRepository, mutedUserRepository

class Services:
    def __init__(self):
        self.chat_repo = ChatRepository()
        self.user_repo = UserRepository()
        self.role_repo = RoleRepository()
        self.comd_repo = CommandRepository()
        self.mesg_repo = MessageRepository()
        self.mute_repo = mutedUserRepository()
    
    def get_commands_by_chat(self, chat_id):
        return self.comd_repo.get_commands_by_chat(chat_id)
    
    def get_commands_by_chat_user(self, chat_id, user_id):
        return self.comd_repo.get_commands_by_chat_user(chat_id, user_id)
    
    def get_chat_by_id(self, chat_id):
        return self.chat_repo.get_chat(chat_id)  
    
    def get_role_by_chat_user(self, chat_id, user_id):
        return self.role_repo.get_role_by_user(chat_id, user_id)
    
    def get_user_by_id(self, user_id):
        return self.user_repo.get_user(user_id)

    def get_messages_by_chat_user(self, chat_id, user_id):
        return self.mesg_repo.get_messages(chat_id, user_id)
    
    def save_message(self, message_id, chat_id, user_id, message, message_type, date):
        return self.mesg_repo.create_message(DTO.Message(
            message_id=message_id,
            user_id=user_id,
            chat_id=chat_id,
            message=message,
            message_type=message_type,
            date=date
        ))
    
    def new_chat(self, chat_id, chat_name):
        return self.chat_repo.create_chat(DTO.Chat(
            id=chat_id,
            chat_name=chat_name,
            spam_mute_time=60,
            spam_message=10,
            spam_time=10,
            delete_pattern="http[s]?://\S+|www\.\S+"
        ))
    
    def add_user(self, user_id, username):
        user = self.user_repo.create_user(DTO.User(
            id=user_id,
            username=username
        ))
        if user:
            return true
    
    def add_user_by_chat(self, user_id, chat_id, role):
        user_chat = self.chat_repo.add_user_by_chat(DTO.UserChat(
            user_id=user_id,
            chat_id=chat_id,
            role_id=self.role_repo.get_role_by_name(chat_id, role).id,
            join_date=date.today().isoformat()
        ))
        if user_chat:
            return true
        
    def get_mute_user(self, user_id, chat_id):
        return self.mute_repo.get_user_mute_by_chat_user(chat_id, user_id)