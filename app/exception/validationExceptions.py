class ValidationError(Exception):
    """Ошибки валидации входных данных."""
    default_message = "Введенные данные некорректны."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)

class ValidationMentionUser(ValidationError):
    default_message = 'Необходимо указать пользователя. @username'

class ValidationDatetime(ValidationError):
    default_message = 'Необходимо указать время. Пример 2001-01-01 или 01:01 или 1h, 1m, 1d, 1w или все вместе'

class ValidationQuotedText(ValidationError):
    default_message = 'Необходимо указать причину. Пример \"Нам такой не нужен\"'

class ValidationMessage(ValidationError):
    default_message = 'Необходимо указать, какое сообщение вы хотите удалить. Пример ответе на сообщение пользователя'