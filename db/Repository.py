from typing import List, Optional
from contextlib import contextmanager
from db.Entity import Chat, Role, Command, RolePermission, User, Message, UserChat  # Импортируем сущности
from db.SQLAlchemy import DBConnection

class RepositoryBase:
    def __init__(self):
        self.session = DBConnection.get_session()  # Просто получаем объект сессии, не вызываем его

    @contextmanager
    def session_scope(self):
        """Предоставляет транзакционную область вокруг серии операций."""
        session = self.session
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class ChatRepository(RepositoryBase):

    def create_chat(self, chat: Chat) -> Chat:
        with self.session_scope() as session:
            session.add(chat)
        return chat

    def get_chat(self, chat_id: int) -> Optional[Chat]:
        with self.session_scope() as session:
            return session.query(Chat).filter(Chat.id == chat_id).first()

    def update_chat(self, chat: Chat) -> Optional[Chat]:
        with self.session_scope() as session:
            existing_chat = session.query(Chat).filter(Chat.id == chat.id).first()
            if existing_chat:
                existing_chat.chat_name = chat.chat_name
            return existing_chat

    def delete_chat(self, chat_id: int) -> bool:
        with self.session_scope() as session:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                session.delete(chat)
                return True
            return False

    def list_chats(self) -> List[Chat]:
        with self.session_scope() as session:
            return session.query(Chat).all()


class RoleRepository(RepositoryBase):

    def create_role(self, role: Role) -> Role:
        with self.session_scope() as session:
            session.add(role)
        return role

    def add_user_role(self, user_id: int, chat_id: int, role_name: str) -> Role:
        new_role = Role(user_id=user_id, chat_id=chat_id, role_name=role_name)
        with self.session_scope() as session:
            session.add(new_role)
        return new_role

    def get_role(self, role_id: int) -> Optional[Role]:
        with self.session_scope() as session:
            return session.query(Role).filter(Role.id == role_id).first()

    def get_role_user_form_chat(self, chat_id: int, user_id: int) -> Optional[Role]:
        with self.session_scope() as session:
            return session.query(Role).filter(Role.chat_id == chat_id, Role.user_id == user_id).first()

    def update_role(self, role: Role) -> Optional[Role]:
        with self.session_scope() as session:
            existing_role = session.query(Role).filter(Role.id == role.id).first()
            if existing_role:
                existing_role.role_name = role.role_name
            return existing_role

    def delete_role(self, role_id: int) -> bool:
        with self.session_scope() as session:
            role = session.query(Role).filter(Role.id == role_id).first()
            if role:
                session.delete(role)
                return True
            return False

    def list_roles(self) -> List[Role]:
        with self.session_scope() as session:
            return session.query(Role).all()


class UserRepository(RepositoryBase):

    def create_user(self, user: User) -> User:
        with self.session_scope() as session:
            session.add(user)
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        with self.session_scope() as session:
            return session.query(User).filter(User.id == user_id).first()

    def get_users(self, users_ids: List[int]) -> Optional[List[User]]:
        with self.session_scope() as session:
            users = session.query(User).filter(User.id.in_(users_ids)).all()
            return users if users else None

    def update_user(self, user: User) -> Optional[User]:
        with self.session_scope() as session:
            existing_user = session.query(User).filter(User.id == user.id).first()
            if existing_user:
                existing_user.username = user.username
            return existing_user

    def delete_user(self, user_id: int) -> bool:
        with self.session_scope() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                return True
            return False

    def list_users(self) -> List[User]:
        with self.session_scope() as session:
            return session.query(User).all()


class MessageRepository(RepositoryBase):

    def create_message(self, message: Message) -> Message:
        with self.session_scope() as session:
            session.add(message)
        return message

    def get_message(self, message_id: int) -> Optional[Message]:
        with self.session_scope() as session:
            return session.query(Message).filter(Message.id == message_id).first()

    def update_message(self, message: Message) -> Optional[Message]:
        with self.session_scope() as session:
            existing_message = session.query(Message).filter(Message.id == message.id).first()
            if existing_message:
                existing_message.message = message.message
            return existing_message

    def delete_message(self, message_id: int) -> bool:
        with self.session_scope() as session:
            message = session.query(Message).filter(Message.id == message_id).first()
            if message:
                session.delete(message)
                return True
            return False

    def list_messages(self, chat_id: int) -> List[Message]:
        with self.session_scope() as session:
            return session.query(Message).filter(Message.chat_id == chat_id).all()


class CommandRepository(RepositoryBase):

    def create_command(self, command: Command) -> Command:
        with self.session_scope() as session:
            session.add(command)
        return command

    def get_command(self, command_id: int) -> Optional[Command]:
        with self.session_scope() as session:
            return session.query(Command).filter(Command.id == command_id).first()

    def get_commands_by_chat(self, chat_id: int) -> List[Command]:
        with self.session_scope() as session:
            return session.query(Command).filter(Command.chat_id == chat_id).all()

    def update_command(self, command: Command) -> Optional[Command]:
        with self.session_scope() as session:
            existing_command = session.query(Command).filter(Command.id == command.id).first()
            if existing_command:
                existing_command.command = command.command
                existing_command.command_name = command.command_name
                existing_command.description = command.description
                existing_command.chat_id = command.chat_id
            return existing_command

    def delete_command(self, command_id: int) -> bool:
        with self.session_scope() as session:
            command = session.query(Command).filter(Command.id == command_id).first()
            if command:
                session.delete(command)
                return True
            return False
