from datetime import date
import logging
from Entity import Entity
from DTO import DTO

class Mapper:
    
    @staticmethod
    def chat_to_dto(chat: Entity.Chat) -> DTO.Chat:
        logging.debug(f'Mapping Chat Entity to DTO: {chat}')
        result = DTO.Chat(
            id=chat.id,
            chat_name=chat.chat_name,
        )
        logging.debug(f'Resulting DTO: {result}')
        return result

    @staticmethod
    def role_to_dto(role: Entity.Role) -> DTO.Role:
        logging.debug(f'Mapping Role Entity to DTO: {role}')
        return DTO.Role(
            id=role.id,
            role_name=role.role_name,
            chat_id=role.chat_id
        )

    @staticmethod
    def command_to_dto(command: Entity.Command) -> DTO.Command:
        logging.debug(f'Mapping Command Entity to DTO: {command}')
        return DTO.Command(
            id=command.id,
            command=command.command,
            command_name=command.command_name,
            description=command.description,
            chat_id=command.chat_id
        )

    @staticmethod
    def user_to_dto(user: Entity.User) -> DTO.User:
        logging.debug(f'Mapping User Entity to DTO: {user}')
        return DTO.User(
            id=user.id,
            username=user.username
        )

    @staticmethod
    def message_to_dto(message: Entity.Message) -> DTO.Message:
        logging.debug(f'Mapping Message Entity to DTO: {message}')
        return DTO.Message(
            id=message.id,
            user_id=message.user_id,
            chat_id=message.chat_id,
            message=message.message,
            message_type=message.message_type,
            date=message.date.isoformat() if message.date else None
        )

    @staticmethod
    def user_chat_to_dto(user_chat: Entity.UserChat) -> DTO.UserChat:
        logging.debug(f'Mapping UserChat Entity to DTO: {user_chat}')
        return DTO.UserChat(
            user_id=user_chat.user_id,
            chat_id=user_chat.chat_id,
            role_id=user_chat.role_id,
            join_date=user_chat.join_date.isoformat() if user_chat.join_date else None
        )
        
    @staticmethod
    def role_per_to_dto(role_permision: Entity.RolePermission) -> DTO.RolePermission:
        logging.debug(f'Mapping RolePremission Entity to DTO: {role_permision}')
        return DTO.RolePermission(
            role_id=role_permision.role_id,
            command_id=role_permision.command_id
        )

    @staticmethod
    def chat_to_entity(chat: DTO.Chat) -> Entity.Chat:
        logging.debug(f'Mapping Chat DTO to Entity {chat}')
        return Entity.Chat(
            id=chat.id,
            chat_name=chat.chat_name,
        )

    @staticmethod
    def role_to_entity(role: DTO.Role) -> Entity.Role:
        logging.debug(f'Mapping Role DTO to Entity {role}')
        return Entity.Role(
            id=role.id,
            role_name=role.role_name,
            chat_id=role.chat_id
        )

    @staticmethod
    def command_to_entity(command: DTO.Command) -> Entity.Command:
        logging.debug(f'Mapping Command DTO to Entity {command}')
        return Entity.Command(
            id=command.id,
            command=command.command,
            command_name=command.command_name,
            description=command.description,
            chat_id=command.chat_id
        )

    @staticmethod
    def user_to_entity(user: DTO.User) -> Entity.User:
        logging.debug(f'Mapping User DTO to Entity {user}')
        return Entity.User(
            id=user.id,
            username=user.username
        )

    @staticmethod
    def message_to_entity(message: DTO.Message) -> Entity.Message:
        logging.debug(f'Mapping Message DTO to Entity {message}')
        return Entity.Message(
            id=message.id,
            user_id=message.user_id,
            chat_id=message.chat_id,
            message=message.message,
            message_type=message.message_type,
            date=date.fromisoformat(message.date) if message.date else None
        )

    @staticmethod
    def user_chat_to_entity(user_chat: DTO.UserChat) -> Entity.UserChat:
        logging.debug(f'Mapping UserChat DTO to Entity {user_chat}')
        return Entity.UserChat(
            user_id=user_chat.user_id,
            chat_id=user_chat.chat_id,
            role_id=user_chat.role_id,
            join_date=date.fromisoformat(user_chat.join_date) if user_chat.join_date else None
        )

    @staticmethod
    def role_per_to_entity(role_permision: DTO.RolePermission) -> Entity.RolePermission:
        logging.debug(f'Mapping RolePermission DTO to Entity {role_permision}')
        return Entity.RolePermission(
            role_id=role_permision.role_id,
            command_id=role_permision.command_id
        )