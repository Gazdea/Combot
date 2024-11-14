from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from models.DTO import MessageDTO, UserDTO, RoleDTO
from service import ChatService, RoleService, UserService, CommandService, MessageService, UserChatService, MutedUserService, RolePermisionService
from .Util import get_mentioned_users, extract_datetime_from_message, get_quoted_text

async def role_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет новую роль в чат."""
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать новую роль. \"role\"')
        return
    RoleService().add_role(RoleDTO(
        role_name=quotes[0],
        chat_id=message.chat.id
    ))
    await message.reply_text(f"Роль добавлена {quotes[0]}.")

async def role_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет роль из чата."""
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать роль. \"role\"')
        return
    role = RoleService().get_role_by_chat_name(message.chat.id, quotes[0])
    if not role:
        await message.reply_text("Роль не найдена.")
        return
    RoleService().delete(role.id)
    await message.reply_text("Роль удалена.")

async def role_command_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет команду в указанную роль."""
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes[0] and not quotes[1]:
        await message.reply_text('Необходимо указать роль и команду в разных. \"role\" \"command\"')
        return
    RolePermisionService().role_command_add(message.chat.id, quotes[0], quotes[1])
    await message.reply_text("Команда добавлена к роли.")

async def role_command_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет команду из указанной роли."""
    message = update.message
    quotes = await get_quoted_text(update, context)
    if not quotes[0] and not quotes[1]:
        await message.reply_text('Необходимо указать роль и команду в разных. \"role\" \"command\"')
        return
    RolePermisionService().role_command_delete(message.chat.id, quotes[0], quotes[1])
    await message.reply_text("Команда удалена из роли.")

async def role_user_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Назначает роль пользователю."""
    message = update.message
    users = await get_mentioned_users(update, context)
    if not users:
        await message.reply_text('Необходимо указать пользователя. \"@username\"')
        return
    quotes = await get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать роль. \"role\"')
        return
    for user in users:
        UserChatService().set_user_role(message.chat.id, user.id, quotes[0])
    await message.reply_text("Роль назначена пользователю.")
