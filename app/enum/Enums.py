from dataclasses import dataclass
from enum import Enum
from typing import List


class UserRole(Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    USER = "USER"
    GUEST = "GUEST"


@dataclass
class CommandDetails:
    show_in_help: bool
    full_description: str
    short_description: str
    triggers: List[str]
    allowed_roles: List[UserRole]


class Command(Enum):
    START = CommandDetails(
        show_in_help=True,
        full_description="Проверяет роботоспособность бота Ping? Pong?",
        short_description="Проверка",
        triggers=["start", "s"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST]
    )

    HELP = CommandDetails(
        show_in_help=True,
        full_description="Показывает список доступных команд, и так же позволяет узнать о каждой команде больше",
        short_description="Помощь, для точности напиши '/help' \"help\"",
        triggers=["help", "h"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST]
    )

    INFO = CommandDetails(
        show_in_help=True,
        full_description="Показывает информацию о бот и его создателе",
        short_description="Информация о боте",
        triggers=["info", "i"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST]
    )

    FAQ = CommandDetails(
        show_in_help=True,
        full_description="Показывает интересные факты",
        short_description="FAQ",
        triggers=["faq"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST]
    )

    DELETE_MESSAGE = CommandDetails(
        show_in_help=True,
        full_description="Удалить сообщение, для этого ответе на сообщение",
        short_description="Удаляет сообщение",
        triggers=["delete", "d"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR]
    )

    BAN = CommandDetails(
        show_in_help=True,
        full_description="Забанить пользователя, укажите пользователя @username укажите дату, или время для бана "
                         "(если указать меньше чем 1 минута то бан будет на всегда), "
                         "и укажите причину \"Причина\"",
        short_description="Банит пользователя",
        triggers=["ban", "b"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR]
    )

    KICK = CommandDetails(
        show_in_help=True,
        full_description="Кикнуть пользователя, укажите пользователя @username и укажите причину \"Причина\"",
        short_description="Кикнуть пользователя",
        triggers=["kick", "k"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR]
    )
    MUTE = CommandDetails(
        show_in_help=True,
        full_description="Замутить пользователя, укажите пользователя @username укажите дату, или время для мута "
                         "(если указать меньше чем 1 минута то мут будет на всегда), "
                         "и укажите причину \"Причина\"",
        short_description="Замутить пользователя",
        triggers=["mute", "m"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR]
    )
    UNMUTE = CommandDetails(
        show_in_help=True,
        full_description="Размутить пользователя, снимает мут что еще сказать",
        short_description="Размутить пользователя",
        triggers=["unmute", "um"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR]
    )

    UNBAN = CommandDetails(
        show_in_help=True,
        full_description="Разбанить пользователя",
        short_description="Разбанить пользователя",
        triggers=["unban", "ub"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR]
    )

    USER_INFO = CommandDetails(
        show_in_help=True,
        full_description="Показывает информацию о пользователе",
        short_description="Информация о пользователе",
        triggers=["user", "u"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR]
    )

    USER_ROLE = CommandDetails(
        show_in_help=True,
        full_description="Показывает роль пользователя, и позволяет изменить ее укажи те @username \"новая роль, user, moderator, guest, admin\"",
        short_description="Роль пользователя",
        triggers=["role", "r"],
        allowed_roles=[UserRole.ADMIN]
    )

    CHAT_USER_JOIN = CommandDetails(
        show_in_help=True,
        full_description="Информация о подключениях к чату",
        short_description="Информация о подключению к чату",
        triggers=["join", "j"],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR]
    )

    CHAT_USER_ACTIVE = CommandDetails(
        show_in_help=True,
        full_description="Информация о активности пользователей",
        short_description="Информация о активности пользователей",
        triggers=["active", "a"],
        allowed_roles=[UserRole.ADMIN]
    )

    CHAT_SPAM_MUTE_TIME = CommandDetails(
        show_in_help=True,
        full_description="Позволяет узнать или поставить время мута за спам в чате, \"10\"",
        short_description="Время мута от спама",
        triggers=["spamMuteTime", "smt"],
        allowed_roles=[UserRole.ADMIN]
    )

    CHAT_SPAM_MESSAGE = CommandDetails(
        show_in_help=True,
        full_description="Позволяет узнать или поставить кол-во сообщения до спама, \"10\"",
        short_description="Колличество сообщения для спама",
        triggers=["spamMessage", "sm"],
        allowed_roles=[UserRole.ADMIN]
    )

    CHAT_DELETE_PATTERN = CommandDetails(
        show_in_help=True,
        full_description="позволяет поставить паттерн для сообщений которые удаляются, \"http[s]?://\S+|www\.\S+\" - стандартное значение, удаляет ссылки",
        short_description="паттерн удаления сообщений",
        triggers=["pattern", "p"],
        allowed_roles=[UserRole.ADMIN]
    )

    DEBUG = CommandDetails(
        show_in_help=False,
        full_description="debug - ну дебаг и дебаг че воротить то",
        short_description="debug",
        triggers=["debug"],
        allowed_roles=[UserRole.ADMIN]
    )

    UNKNOWN = CommandDetails(
        show_in_help=False,
        full_description="unknown",
        short_description="unknown",
        triggers=[],
        allowed_roles=[UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST]
    )

    @property
    def show_in_help(self):
        return self.value.show_in_help

    @property
    def short_description(self):
        return self.value.short_description

    @property
    def full_description(self):
        return self.value.full_description

    @property
    def triggers(self):
        return self.value.triggers

    @property
    def allowed_roles(self):
        return self.value.allowed_roles


bot_help = {
    role.value: [
        {
            "triggers": command.triggers,
            "short_description": command.short_description,
            "full_description": command.full_description,
        }
        for command in Command
        if role in command.allowed_roles and command.show_in_help
    ]
    for role in UserRole
}
