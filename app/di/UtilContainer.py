from dependency_injector import containers, providers
from app.di.ServiceDBContainer import ServiceDBContainer

from app.util.impl import (
    UtilImpl
)

class UtilContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["main"])
    
    
    util = providers.Factory(UtilImpl)