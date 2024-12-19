from dependency_injector import containers, providers
from app.di.ServiceDBContainer import ServiceDBContainer
from app.di.UtilContainer import UtilContainer

from app.bot.handler.impl import (
    HandlerImpl,
    DebugImpl
)

class HandlerContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["main"])
    
    service_container = providers.Container(ServiceDBContainer)
    util_container = providers.Container(UtilContainer)
    
    debug_handler = providers.Factory(DebugImpl, service_container.user_service, util_container.bot_util)
    
    command_handler = providers.Factory(
        HandlerImpl, 
        service_container.command_service, 
        service_container.muted_user_service,
        service_container.user_service,
        service_container.chat_service,
        service_container.user_chat_service,
        service_container.message_service
        )

    