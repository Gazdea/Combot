
def get_banned_user_service():
    from .ServiceDBContainer import ServiceDBContainer
    return ServiceDBContainer.banned_user_service()

def get_chat_service():
    from .ServiceDBContainer import ServiceDBContainer
    return ServiceDBContainer.chat_service()

def get_message_service():
    from .ServiceDBContainer import ServiceDBContainer
    return ServiceDBContainer.message_service()

def get_muted_user_service():
    from .ServiceDBContainer import ServiceDBContainer
    return ServiceDBContainer.muted_user_service()

def get_user_chat_service():
    from .ServiceDBContainer import ServiceDBContainer
    return ServiceDBContainer.user_chat_service()

def get_user_service():
    from .ServiceDBContainer import ServiceDBContainer
    return ServiceDBContainer.user_service()

