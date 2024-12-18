class BusinessError(Exception):
    """Общие исключения для ошибок бизнес-логики."""
    default_message = "Ошибка в бизнес-логике приложения."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)

class InvalidOperationError(BusinessError):
    """Операция недопустима в текущем состоянии."""
    default_message = "Данная операция недопустима."
