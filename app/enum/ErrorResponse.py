from enum import Enum
    
class ChatEnum(Enum):
    NotFound = {"code": 404, "en": "Chat not found", "ru":"Чат не найден"},
    InternalServerError = {"code": 500, "en": "Internal server error", "ru":"Внутренняя ошибка сервера"},
    BadRequest = {"code": 400, "en": "Bad request", "ru":"Неправильный запрос"},
    Forbidden = {"code": 403, "en": "Forbidden", "ru":"Запрещено"},
    Unauthorized = {"code": 401, "en": "Unauthorized", "ru":"Не авторизован"}
    
class UserEnum(Enum):
    NotFound = {"code": 404, "en": "User not found", "ru":"Пользователь не найден"},
    InternalServerError = {"code": 500, "en": "Internal server error", "ru":"Внутренняя ошибка сервера"},
    BadRequest = {"code": 400, "en": "Bad request", "ru":"Неправильный запрос"},
    Forbidden = {"code": 403, "en": "Forbidden", "ru":"Запрещено"},
    Unauthorized = {"code": 401, "en": "Unauthorized", "ru":"Не авторизован"}
    
class CommandEnum(Enum):
    NotFound = {"code": 404, "en": "Command not found", "ru":"Команда не найдена"},
    NotFounds = {"code": 404, "en": "Commands not found", "ru":"Команды не найдены"},
    NotFoundRole = {"code": 404, "en": "Role not found", "ru":"Роль не найдена"},
    InternalServerError = {"code": 500, "en": "Internal server error", "ru":"Внутренняя ошибка сервера"},
    BadRequest = {"code": 400, "en": "Bad request", "ru":"Неправильный запрос"},
    Forbidden = {"code": 403, "en": "Forbidden", "ru":"Запрещено"},
    Unauthorized = {"code": 401, "en": "Unauthorized", "ru":"Не авторизован"}

class MessageEnum(Enum):
    NotFound = {"code": 404, "en": "Message not found", "ru":"Сообщение не найдено"},
    InternalServerError = {"code": 500, "en": "Internal server error", "ru":"Внутренняя ошибка сервера"},
    BadRequest = {"code": 400, "en": "Bad request", "ru":"Неправильный запрос"},
    Forbidden = {"code": 403, "en": "Forbidden", "ru":"Запрещено"},
    Unauthorized = {"code": 401, "en": "Unauthorized", "ru":"Не авторизован"}
    
class RoleEnum(Enum):
    NotFound = {"code": 404, "en": "Role not found", "ru":"Роль не найдена"},
    NotFounds = {"code": 404, "en": "Roles not found", "ru":"Роли не найдены"},
    InternalServerError = {"code": 500, "en": "Internal server error", "ru":"Внутренняя ошибка сервера"},
    BadRequest = {"code": 400, "en": "Bad request", "ru":"Неправильный запрос"},
    Forbidden = {"code": 403, "en": "Forbidden", "ru":"Запрещено"},
    Unauthorized = {"code": 401, "en": "Unauthorized", "ru":"Не авторизован"}
    
class RolePermissionEnum(Enum):
    NotFound = {"code": 404, "en": "Role permission not found", "ru":"Роль не найдена"},
    NotFoundRole = {"code": 404, "en": "Role not found", "ru":"Роль не найдена"},
    NotFoundCommand = {"code": 404, "en": "Command not found", "ru":"Команда не найдена"},
    InternalServerError = {"code": 500, "en": "Internal server error", "ru":"Внутренняя ошибка сервера"},
    BadRequest = {"code": 400, "en": "Bad request", "ru":"Неправильный запрос"},
    Forbidden = {"code": 403, "en": "Forbidden", "ru":"Запрещено"},
    Unauthorized = {"code": 401, "en": "Unauthorized", "ru":"Не авторизован"}
    
class UserChatEnum(Enum):
    NotFound = {"code": 404, "en": "User chat not found", "ru":"Пользователь не найден"},
    NotFounds = {"code": 404, "en": "User chats not found", "ru":"Пользователи не найдены"},
    NotFoundRole = {"code": 404, "en": "Role not found", "ru":"Роль не найдена"},
    InternalServerError = {"code": 500, "en": "Internal server error", "ru":"Внутренняя ошибка сервера"},
    BadRequest = {"code": 400, "en": "Bad request", "ru":"Неправильный запрос"},
    Forbidden = {"code": 403, "en": "Forbidden", "ru":"Запрещено"},
    Unauthorized = {"code": 401, "en": "Unauthorized", "ru":"Не авторизован"}
    
class BannedUserEnum(Enum):
    NotFound = {"code": 404, "en": "Banned user not found", "ru":"Пользователь не найден"},
    InternalServerError = {"code": 500, "en": "Internal server error", "ru":"Внутренняя ошибка сервера"},
    BadRequest = {"code": 400, "en": "Bad request", "ru":"Неправильный запрос"},
    Forbidden = {"code": 403, "en": "Forbidden", "ru":"Запрещено"},
    Unauthorized = {"code": 401, "en": "Unauthorized", "ru":"Не авторизован"}

class MutedUserEnum(Enum):
    NotFound = {"code": 404, "en": "Muted user not found", "ru":"Пользователь не найден"},
    InternalServerError = {"code": 500, "en": "Internal server error", "ru":"Внутренняя ошибка сервера"},
    BadRequest = {"code": 400, "en": "Bad request", "ru":"Неправильный запрос"},
    Forbidden = {"code": 403, "en": "Forbidden", "ru":"Запрещено"},
    Unauthorized = {"code": 401, "en": "Unauthorized", "ru":"Не авторизован"}