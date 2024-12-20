import re
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from app.db.model.DTO import MessageDTO, UserDTO
from app.di.ServiceDBContainer import ServiceDBContainer
from app.di.UtilContainer import UtilContainer

service_container = ServiceDBContainer
util_container = UtilContainer


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получить список возможных команд"""
    # command_service = service_container.command_service()
    
    # message = update.message
    # available_commands = command_service.get_commands_by_chat_user(
    #     message.chat.id, message.from_user.id
    # )
    # available_commands = available_commands
    # pattern = r"\{[^{}]+\}"
    # commands = "\n".join([f"{cmd.command} - {re.sub(pattern, "", cmd.description)}" for cmd in available_commands])
    # await message.reply_text(commands)

async def command_rename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Переименовывает команду."""
    # command_service = service_container.command_service()
    # bot_util = util_container.bot_util()
    
    # message = update.message
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes[0] and not quotes[1]:
    #     await message.reply_text('Необходимо указать название команды, и новое название. \"command\" \"new command\"')
    #     return
    # command = command_service.rename_command(message.chat.id, quotes[0], quotes[1])
    # await message.reply_text("Команда переименована.")
    
async def commands_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получить список команд для указанной роли. Для команды нужно указать роль в кавычках"""
    # command_service = service_container.command_service()
    # bot_util = util_container.bot_util()
    
    # message = update.message
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes:
    #     await message.reply_text('Необходимо указать роль.')
    #     return
    # commands = command_service.get_commands_by_chat_roleName(
    #     message.chat.id, quotes[0]
    # )
    # commands = "\n".join([f"{cmd.command} - {cmd.description}" for cmd in commands])
    # await message.reply_text(commands)