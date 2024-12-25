from dependency_injector import containers, providers
from app.config import get_session

from app.db.repository.baseImpl.impl import (
    BannedUserRepositoryImpl,
    ChatRepositoryImpl,
    MessageRepositoryImpl,
    MutedUserRepositoryImpl,
    UserChatRepositoryImpl,
    UserRepositoryImpl
)

class RepositoryContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["main"])
    
    session = providers.Singleton(get_session)

    banned_user_repository = providers.Factory(BannedUserRepositoryImpl, session=session)
    chat_repository = providers.Factory(ChatRepositoryImpl, session=session)
    message_repository = providers.Factory(MessageRepositoryImpl, session=session)
    muted_user_repository = providers.Factory(MutedUserRepositoryImpl, session=session)
    user_chat_repository = providers.Factory(UserChatRepositoryImpl, session=session)
    user_repository = providers.Factory(UserRepositoryImpl, session=session)