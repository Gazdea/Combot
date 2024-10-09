from db.Entity import Chat, Role, Command, User, Message
from db.DTO import ChatDTO, RoleDTO, CommandDTO, UserDTO, MessageDTO

class Mapper:

    @staticmethod
    def chat_to_dto(chat: Chat) -> ChatDTO:
        return ChatDTO(
            id=chat.id,
            chat_name=chat.chat_name,
            roles=[Mapper.role_to_dto(role) for role in chat.roles],
            commands=[Mapper.command_to_dto(command) for command in chat.commands]
        )

    @staticmethod
    def role_to_dto(role: Role) -> RoleDTO:
        return RoleDTO(
            id=role.id,
            role_name=role.role_name,
            chat_id=role.chat_id
        )

    @staticmethod
    def command_to_dto(command: Command) -> CommandDTO:
        return CommandDTO(
            id=command.id,
            command=command.command,
            command_name=command.command_name,
            description=command.description,
            chat_id=command.chat_id
        )

    @staticmethod
    def user_to_dto(user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            username=user.username,
            join_date=user.join_date.isoformat()
        )

    @staticmethod
    def message_to_dto(message: Message) -> MessageDTO:
        return MessageDTO(
            id=message.id,
            user_id=message.user_id,
            chat_id=message.chat_id,
            message=message.message,
            message_type=message.message_type,
            date=message.date.isoformat()
        )
        
    @staticmethod
    def chat_to_entity(chat: ChatDTO) -> Chat:
        return Chat(
            id=chat.id,
            chat_name=chat.chat_name,
            roles=[Mapper.role_to_dto(role) for role in chat.roles],
            commands=[Mapper.command_to_dto(command) for command in chat.commands]
        )

    @staticmethod
    def role_to_entity(role: RoleDTO) -> Role:
        return Role(
            id=role.id,
            role_name=role.role_name,
            chat_id=role.chat_id
        )

    @staticmethod
    def command_to_entity(command: CommandDTO) -> Command:
        return Command(
            id=command.id,
            command=command.command,
            command_name=command.command_name,
            description=command.description,
            chat_id=command.chat_id
        )

    @staticmethod
    def user_to_entity(user: UserDTO) -> User:
        return User(
            id=user.id,
            username=user.username,
            join_date=user.join_date.isoformat()
        )

    @staticmethod
    def message_to_entity(message: MessageDTO) -> Message:
        return Message(
            id=message.id,
            user_id=message.user_id,
            chat_id=message.chat_id,
            message=message.message,
            message_type=message.message_type,
            date=message.date.isoformat()
        )