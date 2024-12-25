from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    USER = "USER"
    GUEST = "GUEST"

class Command(Enum):
    START = "start"
    HELP = "help"
    INFO = "info"
    FAQ = "faq"

    DELETE_MESSAGE = "delete"

    BAN = "ban"
    KICK = "kick"
    MUTE = "mute"
    UNBAN = "unban"
    UNMUTE = "unmute"
    USER_INFO = "userInfo"
    USER_ROLE = "userRole"

    CHAT_SPAM_MUTE_TIME = "spamMuteTime"

    DEBUG = "debug"
    UNKNOWN = "unknown"


COMMAND_ACCESS = {
    Command.UNKNOWN: [UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST],
    Command.START: [UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST],
    Command.HELP: [UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST],
    Command.INFO: [UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST],
    Command.FAQ: [UserRole.ADMIN, UserRole.MODERATOR, UserRole.USER, UserRole.GUEST],

    Command.DELETE_MESSAGE: [UserRole.ADMIN, UserRole.MODERATOR],
    Command.BAN: [UserRole.ADMIN, UserRole.MODERATOR],
    Command.KICK: [UserRole.ADMIN, UserRole.MODERATOR],
    Command.MUTE: [UserRole.ADMIN, UserRole.MODERATOR],
    Command.USER_INFO: [UserRole.ADMIN, UserRole.MODERATOR],
    Command.UNBAN: [UserRole.ADMIN, UserRole.MODERATOR],
    Command.UNMUTE: [UserRole.ADMIN, UserRole.MODERATOR],

    Command.USER_ROLE: [UserRole.ADMIN],
    Command.DEBUG: [UserRole.ADMIN],
}

bot_help = {
    role.value: "\n".join(
        f"/{command.value} - {command.name.capitalize()}"
        for command, roles in COMMAND_ACCESS.items()
        if role in roles
    )
    for role in UserRole
}