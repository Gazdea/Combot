class BusinessError(Exception):
    """Общие исключения для ошибок бизнес-логики."""
    default_message = "Ошибка в бизнес-логике приложения."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)

class InvalidOperationError(BusinessError):
    """Операция недопустима в текущем состоянии."""
    default_message = "Данная операция недопустима."

class NotFound(BusinessError):
    """Не удалось найти."""
    default_message = "Не удалось найти."
    
class NotFoundUser(NotFound):
    """Не удалсь найти пользователя"""
    default_message = "Не удалось найти пользователя."
    
class NotFoundChat(NotFound):
    """Не удалось найти чат"""
    default_message = "Не удалось найти чат."