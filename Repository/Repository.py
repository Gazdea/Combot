import logging
from typing import List, Optional
from contextlib import contextmanager
from Entity.Entity import Chat, Role, Command, RolePermission, User, Message, UserChat  # Импортируем сущности
from Connection.SQLAlchemy import DBConnection
from sqlalchemy.orm import Session
from Mapper.Mapper import Mapper  # Импортируем маппер


class RepositoryBase:
    @contextmanager
    def session_scope(self) -> Session:
        """Контекстный менеджер для работы с сессией."""
        session = DBConnection.get_session()  # Создаем новую сессию для каждой транзакции
        try:
            yield session
            session.commit()  # Коммит транзакции
        except Exception as e:
            logging.error(f'Error occurred: {e}', exc_info=True)
            session.rollback()  # Откат транзакции при ошибке
            raise e
        finally:
            session.close()  # Закрытие сессии после завершения


class ChatRepository(RepositoryBase):
    def create_chat(self, chat_dto) -> Chat:
        chat = Mapper.chat_to_entity(chat_dto)
        with self.session_scope() as session:
            session.merge(chat)
            session.flush()
            return Mapper.chat_to_dto(chat)  # Возвращаем DTO

    def add_user_by_chat(self, user_chat_dto) -> UserChat:
        user_chat = Mapper.user_chat_to_entity(user_chat_dto)
        with self.session_scope() as session:
            session.merge(user_chat)
            session.flush()
            return Mapper.user_chat_to_dto(user_chat)  # Возвращаем DTO

    def get_chat(self, chat_id: int) -> Optional[Chat]:
        with self.session_scope() as session:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            return Mapper.chat_to_dto(chat) if chat else None  # Возвращаем DTO

    def update_chat(self, chat_dto) -> Optional[Chat]:
        chat = Mapper.chat_to_entity(chat_dto)
        with self.session_scope() as session:
            existing_chat = session.query(Chat).filter(Chat.id == chat.id).first()
            if existing_chat:
                existing_chat.chat_name = chat.chat_name
            return Mapper.chat_to_dto(existing_chat) if existing_chat else None  # Возвращаем DTO

    def delete_chat(self, chat_id: int) -> bool:
        with self.session_scope() as session:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                session.delete(chat)
                return True
            return False

    def list_chats(self) -> List[Chat]:
        with self.session_scope() as session:
            chats = session.query(Chat).all()
            return [Mapper.chat_to_dto(chat) for chat in chats]  # Возвращаем список DTO


class RoleRepository(RepositoryBase):
    def add_role(self, role_dto) -> Role:
        role = Mapper.role_to_entity(role_dto)
        with self.session_scope() as session:
            session.merge(role)
            session.flush()
            return Mapper.role_to_dto(role)  # Возвращаем DTO

    def get_role_by_user(self, chat_id: int, user_id: int) -> Optional[Role]:
        with self.session_scope() as session:
            user_chat = session.query(UserChat).filter(UserChat.chat_id == chat_id, UserChat.user_id == user_id).first()
            return Mapper.role_to_dto(user_chat.role) if user_chat else None  # Возвращаем DTO

    def get_role_by_name(self, chat_id: int, name: str) -> Optional[Role]:
        with self.session_scope() as session:
            return Mapper.role_to_dto(session.query(Role).filter(Role.chat_id == chat_id, Role.role_name == name).first())

    def update_role(self, role_dto) -> Optional[Role]:
        role = Mapper.role_to_entity(role_dto)
        with self.session_scope() as session:
            existing_role = session.query(Role).filter(Role.id == role.id).first()
            if existing_role:
                existing_role.role_name = role.role_name
            return Mapper.role_to_dto(existing_role) if existing_role else None  # Возвращаем DTO

    def delete_role(self, role_id: int) -> bool:
        with self.session_scope() as session:
            role = session.query(Role).filter(Role.id == role_id).first()
            if role:
                session.delete(role)
                return True
            return False

    def list_roles_by_chat(self, chat_id: int) -> List[Role]:
        with self.session_scope() as session:
            roles = session.query(Role).filter(Role.chat_id == chat_id).all()
            return [Mapper.role_to_dto(role) for role in roles]  # Возвращаем список DTO


class UserRepository(RepositoryBase):
    def create_user(self, user_dto) -> User:
        user = Mapper.user_to_entity(user_dto)
        with self.session_scope() as session:
            # Проверяем, существует ли уже пользователь
            existing_user = session.query(User).filter(User.id == user.id).first()
            if not existing_user:  # Если пользователь не существует
                session.merge(user)  # Добавляем нового пользователя
                session.flush()
                return Mapper.user_to_dto(user)  # Возвращаем DTO для только что добавленного пользователя
            return Mapper.user_to_dto(existing_user)  # Если пользователь существует, возвращаем его DTO

    def get_user(self, user_id: int) -> Optional[User]:
        with self.session_scope() as session:
            return Mapper.user_to_dto(session.query(User).filter(User.id == user_id).first())

    def get_users(self, users_ids: List[int]) -> List[User]:
        with self.session_scope() as session:
            return [Mapper.user_to_dto(user) for user in session.query(User).filter(User.id.in_(users_ids)).all()] or []

    def update_user(self, user_dto) -> Optional[User]:
        user = Mapper.user_to_entity(user_dto)
        with self.session_scope() as session:
            existing_user = session.query(User).filter(User.id == user.id).first()
            if existing_user:
                existing_user.username = user.username
            return Mapper.user_to_dto(existing_user) if existing_user else None  # Возвращаем DTO

    def delete_user(self, user_id: int) -> bool:
        with self.session_scope() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                return True
            return False

    def list_users(self) -> List[User]:
        with self.session_scope() as session:
            users = session.query(User).all()
            return [Mapper.user_to_dto(user) for user in users]  # Возвращаем список DTO


class MessageRepository(RepositoryBase):
    def create_message(self, message_dto) -> Message:
        message = Mapper.message_to_entity(message_dto)
        with self.session_scope() as session:
            session.merge(message)
            session.flush()
            return Mapper.message_to_dto(message)  # Возвращаем DTO

    def get_messages(self, chat_id: int, user_id: int) -> List[Message]:
        with self.session_scope() as session:
            return [Mapper.message_to_dto(message) for message in session.query(Message).filter(Message.chat_id == chat_id, Message.user_id == user_id).all()]

    def update_message(self, message_dto) -> Optional[Message]:
        message = Mapper.message_to_entity(message_dto)
        with self.session_scope() as session:
            existing_message = session.query(Message).filter(Message.id == message.id).first()
            if existing_message:
                existing_message.message = message.message
            return Mapper.message_to_dto(existing_message) if existing_message else None  # Возвращаем DTO

    def delete_message(self, message_id: int) -> bool:
        with self.session_scope() as session:
            message = session.query(Message).filter(Message.id == message_id).first()
            if message:
                session.delete(message)
                return True
            return False

    def list_messages(self, chat_id: int) -> List[Message]:
        with self.session_scope() as session:
            messages = session.query(Message).filter(Message.chat_id == chat_id).all()
            return [Mapper.message_to_dto(message) for message in messages]  # Возвращаем список DTO


class CommandRepository(RepositoryBase):
    def create_command(self, command_dto) -> Command:
        command = Mapper.command_to_entity(command_dto)
        with self.session_scope() as session:
            session.merge(command)
            session.flush()
            return Mapper.command_to_dto(command)  # Возвращаем DTO

    def get_command(self, command_id: int) -> Optional[Command]:
        with self.session_scope() as session:
            return Mapper.command_to_dto(session.query(Command).filter(Command.id == command_id).first())

    def get_commands_by_chat(self, chat_id: int) -> List[Command]:
        with self.session_scope() as session:
            commands = session.query(Command).filter(Command.chat_id == chat_id).all()
            return [Mapper.command_to_dto(command) for command in commands]  # Возвращаем список DTO

    def get_commands_by_chat_user(self, chat_id: int, user_id: int) -> List[Command]:
        with self.session_scope() as session:
            commands = (
                session.query(Command)
                .join(RolePermission, RolePermission.command_id == Command.id)
                .join(Role, Role.id == RolePermission.role_id)
                .join(UserChat, UserChat.role_id == Role.id)
                .filter(UserChat.user_id == user_id, UserChat.chat_id == chat_id)
                .all()
            )
            return [Mapper.command_to_dto(command) for command in commands]

    def update_command(self, command_dto) -> Optional[Command]:
        command = Mapper.command_to_entity(command_dto)
        with self.session_scope() as session:
            existing_command = session.query(Command).filter(Command.id == command.id).first()
            if existing_command:
                existing_command.command = command.command
                existing_command.command_name = command.command_name
                existing_command.description = command.description
                existing_command.chat_id = command.chat_id
            return Mapper.command_to_dto(existing_command) if existing_command else None  # Возвращаем DTO

    def delete_command(self, command_id: int) -> bool:
        with self.session_scope() as session:
            command = session.query(Command).filter(Command.id == command_id).first()
            if command:
                session.delete(command)
                return True
            return False
