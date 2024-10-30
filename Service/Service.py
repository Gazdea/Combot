from datetime import date
from sqlalchemy import true

from DTO import DTO
from Repository.Repository import ChatRepository, CommandRepository, MessageRepository, RolePermissionRepository, RoleRepository, UserChatRepository, UserRepository, MutedUserRepository

class Services:
    def __init__(self):
        self.chat_repo = ChatRepository()
        self.user_repo = UserRepository()
        self.role_repo = RoleRepository()
        self.comd_repo = CommandRepository()
        self.mesg_repo = MessageRepository()
        self.mute_repo = MutedUserRepository()
        self.user_chat_repo = UserChatRepository()
        self.role_perm_repo = RolePermissionRepository()
    
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
    
    def save_chat(self, chat_dto):
        return self.chat_repo.update_chat(chat_dto)
    
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
    
    def add_role(self, chat_id, role_name):
        return self.role_repo.add_role(DTO.Role(role_name=role_name, chat_id=chat_id))
    
    def delete_role(self, chat_id, role_name):
        role = self.role_repo.get_role_by_name(chat_id, role_name)
        return self.role_repo.delete_role(role.id)
    
    def role_command_add(self, chat_id, role_name, command_name):
        command = self.comd_repo.get_command_by_name(command_name)
        role = self.role_repo.get_role_by_name(chat_id, role_name)
        return self.role_perm_repo.set_command_by_role(DTO.RolePermission(role_id=role.id, command_id=command.id))
        
    def role_command_delete(self, chat_id, role_name, command_name):
        command = self.comd_repo.get_command_by_name(command_name)
        role = self.role_repo.get_role_by_name(chat_id, role_name)
        return self.role_repo.delete_command_by_role(DTO.RolePermission(role_id=role.id, command_id=command.id))
    
    def set_user_role(self, chat_id, user_id, role_name):
        role = self.role_repo.get_role_by_name(chat_id, role_name)
        user_chat_dto = self.user_chat_repo.get_user_role(chat_id, user_id)
        user_chat_dto.role_id = role.id
        return self.user_chat_repo.set_user_role(user_chat_dto)
    
    def rename_command(self, chat_id, command_name, new_command_name):
        command_dto = self.comd_repo.get_command_by_name(chat_id, command_name)
        command_dto.command = new_command_name
        return self.comd_repo.update_command(command_dto)
    
    def get_user_chat(self, chat_id, user_id):
        return self.user_chat_repo.get_user_role(chat_id=chat_id, user_id=user_id)
    
    def get_stats_users_join(self, chat_id, date_start = date.today(), date_end = date.today()):
        return self.user_chat_repo.get_join_users(chat_id=chat_id, date_start=date_start, date_end=date_end)
    
    def get_stat_user_message(self, chat_id, user_id, date_start = date.today(), date_end = date.today()):
        return self.mesg_repo.get_count_messages(chat_id, user_id, date_start, date_end)
    
    
    