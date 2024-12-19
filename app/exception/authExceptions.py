class AuthenticationError(Exception):
    """Ошибки аутентификации."""
    default_message = "Ошибка аутентификации пользователя."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)

class AuthorizationError(Exception):
    """Ошибки авторизации."""
    default_message = "У вас нет прав для выполнения данной операции."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)
