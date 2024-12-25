from dependency_injector import containers, providers
from app.db.di.RepositoryContainer import RepositoryContainer

from app.db.service.impl import (
    BannedUserDBServiceImpl,
    ChatDBServiceImpl,
    MessageDBServiceImpl,
    MutedUserDBServiceImpl,
    UserChatDBServiceImpl,
    UserDBServiceImpl
)

class ServiceDBContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["main"])
    repository_container = providers.Container(RepositoryContainer)
    
    banned_user_service = providers.Factory(BannedUserDBServiceImpl, repository_container.banned_user_repository)
    chat_service = providers.Factory(ChatDBServiceImpl, repository_container.chat_repository)
    message_service = providers.Factory(MessageDBServiceImpl, repository_container.message_repository)
    muted_user_service = providers.Factory(MutedUserDBServiceImpl, repository_container.muted_user_repository)
    user_chat_service = providers.Factory(UserChatDBServiceImpl, repository_container.user_chat_repository)
    user_service = providers.Factory(UserDBServiceImpl, repository_container.user_repository)
