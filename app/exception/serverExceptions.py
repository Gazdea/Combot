class ServerError(Exception):
    """Общие исключения для серверных ошибок."""
    default_message = "Произошла ошибка на сервере."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)

class DatabaseConnectionError(ServerError):
    """Ошибка подключения к базе данных."""
    default_message = "Не удалось подключиться к базе данных."

class TelegramAPIError(ServerError):
    default_message = "Не удалось подключиться к телеграмм API"