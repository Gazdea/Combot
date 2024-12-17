from dependency_injector import containers, providers
from app.di import ServiceContainer

from app.bot.util.impl import (
    UtilImpl
)

class UtilContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["main"])
    
    service_container = providers.Container(ServiceContainer)
    
    bot_util = providers.Factory(UtilImpl, service_container.user_service, service_container.command_service)