class ValidationError(Exception):
    """Ошибки валидации входных данных."""
    default_message = "Введенные данные некорректны."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)
