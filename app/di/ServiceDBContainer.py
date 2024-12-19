from dependency_injector import containers, providers
from app.di.RepositoryContainer import RepositoryContainer

from app.db.service.impl import (
    BannedUserDBServiceImpl,
    ChatDBServiceImpl,
    CommandDBServiceImpl,
    MessageDBServiceImpl,
    MutedUserDBServiceImpl,
    RoleDBServiceImpl,
    RolePermissionDBServiceImpl,
    UserChatDBServiceImpl,
    UserDBServiceImpl
)

class ServiceDBContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["main"])
    repository_container = providers.Container(RepositoryContainer)
    
    banned_user_service = providers.Factory(BannedUserDBServiceImpl, repository_container.banned_user_repository)
    chat_service = providers.Factory(ChatDBServiceImpl, repository_container.chat_repository)
    command_service = providers.Factory(CommandDBServiceImpl, repository_container.command_repository, repository_container.role_repository)
    message_service = providers.Factory(MessageDBServiceImpl, repository_container.message_repository)
    muted_user_service = providers.Factory(MutedUserDBServiceImpl, repository_container.muted_user_repository)
    role_service = providers.Factory(RoleDBServiceImpl, repository_container.role_repository)
    role_permission_service = providers.Factory(RolePermissionDBServiceImpl, repository_container.role_permission_repository, repository_container.command_repository, repository_container.role_repository)
    user_chat_service = providers.Factory(UserChatDBServiceImpl, repository_container.user_chat_repository, repository_container.role_repository)
    user_service = providers.Factory(UserDBServiceImpl, repository_container.user_repository)
