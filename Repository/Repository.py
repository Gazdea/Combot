from datetime import date, datetime
from typing import List, Optional
from Models.Entity import BanUser, Chat, Role, Command, RolePermission, User, Message, UserChat, MutedUser
from Models.DTO import BanUserDTO, ChatDTO, CommandDTO, MessageDTO, MutedUsersDTO, RoleDTO, RolePermissionDTO, UserDTO, UserChatDTO
from Repository import RepositoryBase

class ChatRepository(RepositoryBase):
    def create_chat(self, chat_dto: ChatDTO) -> Optional[Chat]:
        chat = Chat(**chat_dto.model_dump())
        with self.session_scope() as session:
            session.merge(chat)
            session.flush()
            return ChatDTO.model_validate(chat)

    def get_chat(self, chat_id: int) -> Optional[Chat]:
        with self.session_scope() as session:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            return ChatDTO.model_validate(chat) if chat else None

    def update_chat(self, chat_dto: ChatDTO) -> Optional[Chat]:
        chat = Chat(**chat_dto.model_dump())
        with self.session_scope() as session:
            existing_chat = session.query(Chat).filter(Chat.id == chat.id).first()
            if existing_chat:
                existing_chat.chat_name = chat.chat_name
            return ChatDTO.model_validate(existing_chat) if existing_chat else None

    def delete_chat(self, chat_id: int) -> Optional[bool]:
        with self.session_scope() as session:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                session.delete(chat)
                return True
            return False

    def list_chats(self) -> List[Chat]:
        with self.session_scope() as session:
            chats = session.query(Chat).all()
            return [ChatDTO.model_validate(chat) for chat in chats]


class RoleRepository(RepositoryBase):
    def add_role(self, role_dto: RoleDTO) -> Optional[Role]:
        role = Role(**role_dto.model_dump())
        with self.session_scope() as session:
            session.merge(role)
            session.flush()
            return ChatDTO.model_validate(role)

    def get_role_by_user(self, chat_id: int, user_id: int) -> Optional[Role]:
        with self.session_scope() as session:
            user_chat = session.query(UserChat).filter(UserChat.chat_id == chat_id, UserChat.user_id == user_id).first()
            return ChatDTO.model_validate(user_chat.role) if user_chat else None
    
    def get_role_by_name(self, chat_id: int, name: str) -> Optional[Role]:
        with self.session_scope() as session:
            return RoleDTO.model_validate(session.query(Role).filter(Role.chat_id == chat_id, Role.role_name == name).first())

    def update_role(self, role_dto: RoleDTO) -> Optional[Role]:
        role = Role(**role_dto.model_dump())
        with self.session_scope() as session:
            existing_role = session.query(Role).filter(Role.id == role.id).first()
            if existing_role:
                existing_role.role_name = role.role_name
            return RoleDTO.model_validate(existing_role) if existing_role else None

    def delete_role(self, role_id: int) -> Optional[bool]:
        with self.session_scope() as session:
            role = session.query(Role).filter(Role.id == role_id).first()
            if role:
                session.delete(role)
                return True
            return False

    def list_roles_by_chat(self, chat_id: int) -> Optional[list[Role]]:
        with self.session_scope() as session:
            roles = session.query(Role).filter(Role.chat_id == chat_id).all()
            return [RoleDTO.model_validate(role) for role in roles]


class UserRepository(RepositoryBase):
    def create_user(self, user_dto: UserDTO) -> Optional[User]:
        user = User(**user_dto.model_dump())
        with self.session_scope() as session:
            session.merge(user)
            session.flush()
            return UserDTO.model_validate(user)

    def get_user(self, user_id: int) -> Optional[User]:
        with self.session_scope() as session:
            return UserDTO.model_validate(session.query(User).filter(User.id == user_id).first())

    def get_users(self, users_ids: List[int]) -> Optional[list[User]]:
        with self.session_scope() as session:
            return [UserDTO.model_validate(user) for user in session.query(User).filter(User.id.in_(users_ids)).all()] or []

    def update_user(self, user_dto: UserDTO) -> Optional[User]:
        user = User(**user_dto.model_dump())
        with self.session_scope() as session:
            existing_user = session.query(User).filter(User.id == user.id).first()
            if existing_user:
                existing_user.username = user.username
            return UserDTO.model_validate(existing_user) if existing_user else None

    def delete_user(self, user_id: int) -> Optional[bool]:
        with self.session_scope() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                return True
            return False

    def list_users(self) -> Optional[list[User]]:
        with self.session_scope() as session:
            users = session.query(User).all()
            return [UserDTO.model_validate(user) for user in users]


class MessageRepository(RepositoryBase):
    def create_message(self, message_dto: MessageDTO) -> Optional[Message]:
        message = Message(**message_dto.model_dump())
        with self.session_scope() as session:
            session.merge(message)
            session.flush()
            return MessageDTO.model_validate(message)

    def get_messages(self, chat_id: int, user_id: int) -> Optional[list[Message]]:
        with self.session_scope() as session:
            return [MessageDTO.model_validate(message) for message in session.query(Message).filter(Message.chat_id == chat_id, Message.user_id == user_id).all()]

    def get_count_messages(self, chat_id: int, user_id: int, date_start: date, date_end: date) -> Optional[int]:
        with self.session_scope() as session:
            return session.query(Message).filter(Message.chat_id == chat_id, Message.user_id == user_id, Message.date >= date_start, Message.date <= date_end).count()

    def update_message(self, message_dto) -> Optional[Message]:
        message = Message(**message_dto.model_dump())
        with self.session_scope() as session:
            existing_message = session.query(Message).filter(Message.id == message.id).first()
            if existing_message:
                existing_message.message = message.message
            return MessageDTO.model_validate(existing_message) if existing_message else None

    def delete_message(self, message_id: int) -> Optional[bool]:
        with self.session_scope() as session:
            message = session.query(Message).filter(Message.id == message_id).first()
            if message:
                session.delete(message)
                return True
            return False

    def list_messages(self, chat_id: int) -> Optional[list[Message]]:
        with self.session_scope() as session:
            messages = session.query(Message).filter(Message.chat_id == chat_id).all()
            return [MessageDTO.model_validate(message) for message in messages]


class CommandRepository(RepositoryBase):
    def create_command(self, command_dto: CommandDTO) -> Optional[Command]:
        command = Command(**command_dto.model_dump())
        with self.session_scope() as session:
            session.merge(command)
            session.flush()
            return CommandDTO.model_validate(command)

    def get_command(self, command_id: int) -> Optional[Command]:
        with self.session_scope() as session:
            return CommandDTO.model_validate(session.query(Command).filter(Command.id == command_id).first())

    def get_command_by_name(self, chat_id, command_name) -> Optional[Command]:
        with self.session_scope() as session:
            return CommandDTO.model_validate(session.query(Command).filter(
                Command.chat_id == chat_id, 
                Command.command == '/' + command_name)
            )
            
    def get_commands_by_chat(self, chat_id: int) -> Optional[list[Command]]:
        with self.session_scope() as session:
            commands = session.query(Command).filter(Command.chat_id == chat_id).all()
            return [CommandDTO.model_validate(command) for command in commands]

    def get_commands_by_chat_user(self, chat_id: int, user_id: int) -> Optional[list[Command]]:
        with self.session_scope() as session:
            commands = (
                session.query(Command)
                .filter(Command.chat_id == chat_id)
                .join(RolePermission, RolePermission.command_id == Command.id)
                .join(Role, Role.id == RolePermission.role_id)
                .join(UserChat, UserChat.role_id == Role.id)
                .filter(UserChat.user_id == user_id)
                .all()
            )
            return [CommandDTO.model_validate(command) for command in commands]

    def update_command(self, command_dto: CommandDTO) -> Optional[Command]:
        command = Command(**command_dto.model_dump())
        with self.session_scope() as session:
            existing_command = session.query(Command).filter(Command.id == command.id).first()
            if existing_command:
                existing_command.command = command.command
            return CommandDTO.model_validate(existing_command) if existing_command else None

    def delete_command(self, command_id: int) -> Optional[bool]:
        with self.session_scope() as session:
            command = session.query(Command).filter(Command.id == command_id).first()
            if command:
                session.delete(command)
                return True
            return False


class RolePermissionRepository(RepositoryBase):
    def set_command_by_role(self, role_permision_dto: RolePermissionDTO) -> Optional[RolePermission]:
        role_permission = RolePermission(**role_permision_dto.model_dump())
        with self.session_scope() as session:
            session.merge(role_permission)
            session.flush()
            return RolePermissionDTO.model_validate(role_permission)
        
    def delete_command_by_role(self, role_permision_dto: RolePermissionDTO) -> Optional[bool]:
        role_permission = RolePermission(**role_permision_dto.model_dump())
        with self.session_scope() as session:
            session.delete(role_permission)
            return True
        return False


class UserChatRepository(RepositoryBase):
    def set_user_role(self, user_chat_dto: UserChatDTO) -> Optional[UserChat]:
        user_chat = UserChat(**user_chat_dto.model_dump)
        with self.session_scope() as session:
            session.merge(user_chat)
            session.flush()
            return UserChatDTO.model_validate(user_chat)
    
    def get_user_role(self, chat_id: int, user_id: int) -> Optional[UserChat]:
        with self.session_scope() as session:
            return UserChatDTO.model_validate(session.query(UserChat).filter(
                UserChat.chat_id == chat_id, 
                UserChat.user_id == user_id).first()
            )

    def get_join_users(self, chat_id: int, date_start: date, date_end: date) -> List[Optional[UserChat]]:
        with self.session_scope() as session:
            return [UserChatDTO.model_validate(user_chat for user_chat in session.query(UserChat).filter(UserChat.chat_id == chat_id, UserChat.join_date >= date_start, UserChat.join_date <= date_end).all)]

    def add_user_by_chat(self, user_chat_dto: UserChatDTO) -> Optional[UserChat]:
        user_chat = UserChat(**user_chat_dto.model_dump)
        with self.session_scope() as session:
            session.merge(user_chat)
            session.flush()
            return UserChatDTO.model_validate(user_chat)


class MutedUserRepository(RepositoryBase):
    def create_user_mute(self, muted_user_dto: MutedUsersDTO) -> Optional[MutedUsersDTO]:
        muted_user = MutedUser(**muted_user_dto.model_dump())
        with self.session_scope() as session:
            session.merge(muted_user)
            session.flush()
            return MutedUsersDTO.model_validate(muted_user)
        
    def get_users_mute_by_chat(self, chat_id: int) -> Optional[list[MutedUsersDTO]]:
        with self.session_scope() as session:
            muted_users = session.query(MutedUser).filter(MutedUser.chat_id == chat_id).all()
            return [MutedUsersDTO.model_validate(muted_user) for muted_user in muted_users]
        
    def get_user_mutes_by_chats(self, user_id: int) -> Optional[list[MutedUsersDTO]]:
        with self.session_scope() as session:
            muted_users = session.query(MutedUser).filter(MutedUser.user_id == user_id).all()
            return [MutedUsersDTO.model_validate(muted_user) for muted_user in muted_users]
        
    def get_user_mute_by_chat_user(self, chat_id: int, user_id: int, start_time: datetime, end_time: datetime) -> Optional[MutedUsersDTO]:
        with self.session_scope() as session:
            muted_user = session.query(MutedUser).filter(
                MutedUser.chat_id == chat_id,
                MutedUser.user_id == user_id,
                MutedUser.time_end >= start_time,
                MutedUser.time_end <= end_time 
            ).first()
            return MutedUsersDTO.model_validate(muted_user) if muted_user else None
        
        
class BannedUserRepository(RepositoryBase):
    def create_user_ban(self, ban_user_dto: BanUserDTO) -> Optional[BanUserDTO]:
        muted_user = BanUserDTO(**ban_user_dto.model_dump())
        with self.session_scope() as session:
            session.merge(muted_user)
            session.flush()
            return BanUserDTO.model_validate(muted_user)
        
    def get_users_ban_by_chat(self, chat_id: int) -> Optional[list[BanUserDTO]]:
        with self.session_scope() as session:
            muted_users = session.query(BanUser).filter(BanUser.chat_id == chat_id).all()
            return [BanUserDTO.model_validate(muted_user) for muted_user in muted_users]
        
    def get_user_bans_by_chats(self, user_id: int) -> Optional[list[BanUserDTO]]:
        with self.session_scope() as session:
            muted_users = session.query(BanUser).filter(BanUser.user_id == user_id).all()
            return [BanUserDTO.model_validate(muted_user) for muted_user in muted_users]
        
    def get_user_ban_by_chat_user(self, chat_id: int, user_id: int) -> Optional[BanUserDTO]:
        with self.session_scope() as session:
            muted_user = session.query(BanUser).filter(
                BanUser.chat_id == chat_id,
                BanUser.user_id == user_id,
                BanUser.time_end > datetime.now()
            ).first()
            return BanUserDTO.model_validate(muted_user) if muted_user else None
        
