from dependency_injector import containers, providers

from app.service.impl import (
    ChatLogicServiceImpl,
    RoleLogicServiceImpl,
    UserLogicServiceImpl,
    CommandLogicServiceImpl,
    MessageLogicServiceImpl,
    StandardLogicServiceImpl
)

class ServiceLogicContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["main"])
    
    chat_logic_service = providers.Factory(ChatLogicServiceImpl)
    role_logic_service = providers.Factory(RoleLogicServiceImpl)
    user_logic_service = providers.Factory(UserLogicServiceImpl)
    command_logic_service = providers.Factory(CommandLogicServiceImpl)
    message_logic_service = providers.Factory(MessageLogicServiceImpl)
    standard_logic_service = providers.Factory(StandardLogicServiceImpl)
    