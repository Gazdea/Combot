from dependency_injector import containers, providers

from app.bot.service.impl import (
    ChatBotServiceImpl,
    RoleBotServiceImpl,
    UserBotServiceImpl,
    CommandBotServiceImpl,
    MessageBotServiceImpl,
    StandardBotServiceImpl
)

class ServiceBotContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["main"])
    
    chat_bot_service = providers.Factory(ChatBotServiceImpl)
    role_bot_service = providers.Factory(RoleBotServiceImpl)
    user_bot_service = providers.Factory(UserBotServiceImpl)
    command_bot_service = providers.Factory(CommandBotServiceImpl)
    message_bot_service = providers.Factory(MessageBotServiceImpl)
    standard_bot_service = providers.Factory(StandardBotServiceImpl)
    