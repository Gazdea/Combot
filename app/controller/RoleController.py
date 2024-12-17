from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from app.db.model.DTO import MessageDTO, UserDTO, RoleDTO
from app.di import ServiceContainer, UtilContainer

service_container = ServiceContainer
util_container = UtilContainer

async def role_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет новую роль в чат."""
    role_service = service_container.role_service()
    bot_util = util_container.bot_util() 
    
    message = update.message
    quotes = await bot_util.get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать новую роль. \"role\"')
        return
    role_service.add_role(RoleDTO(
        role_name=quotes[0],
        chat_id=message.chat.id
    ))
    await message.reply_text(f"Роль добавлена {quotes[0]}.")

async def role_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет роль из чата."""
    role_service = service_container.role_service()
    bot_util = util_container.bot_util() 
    
    message = update.message
    quotes = await bot_util.get_quoted_text(update, context)
    if not quotes:
        await message.reply_text('Необходимо указать роль. \"role\"')
        return
    role = role_service.get_role_by_chat_name(message.chat.id, quotes[0])
    if role.is_error():
        await message.reply_text(role.error)
        return
    role_service.delete(role.value.id)
    if role.is_error():
        await message.reply_text(role.error)
        return
    await message.reply_text("Роль удалена.")

async def role_command_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет команду в указанную роль."""
    role_permission_service = service_container.role_permission_service()
    bot_util = util_container.bot_util() 
    
    message = update.message
    quotes = await bot_util.get_quoted_text(update, context)
    if not quotes[0] and not quotes[1]:
        await message.reply_text('Необходимо указать роль и команду в разных. \"role\" \"command\"')
        return
    role_permission_service.role_command_add(message.chat.id, quotes[0], quotes[1])
    await message.reply_text("Команда добавлена к роли.")

async def role_command_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет команду из указанной роли."""
    role_permission_service = service_container.role_permission_service()
    bot_util = util_container.bot_util() 
    
    message = update.message
    quotes = await bot_util.get_quoted_text(update, context)
    if not quotes[0] and not quotes[1]:
        await message.reply_text('Необходимо указать роль и команду в разных. \"role\" \"command\"')
        return
    role_permission_service.role_command_delete(message.chat.id, quotes[0], quotes[1])
    await message.reply_text("Команда удалена из роли.")

async def role_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает список ролей в чате."""
    role_service = service_container.role_service()
    
    message = update.message
    roles = role_service.get_roles_by_chat(message.chat.id)
    if roles.is_success():
        roles = "\n".join([f"{role.role_name}" for role in roles.value])
        await message.reply_text(roles)
    elif roles.is_error():
        await message.reply_text(roles.error)
        
async def role_rename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Переименовывает роль."""
    role_service = service_container.role_service()
    bot_util = util_container.bot_util() 
    
    message = update.message
    quotes = await bot_util.get_quoted_text(update, context)
    if not quotes[0] and not quotes[1]:
        await message.reply_text('Необходимо указать роль, и новое название. \"role\" \"new role\"')
        return
    role = role_service.role_rename(message.chat.id, quotes[0], quotes[1])
    if role.is_success():
        await message.reply_text("Роль переименована.")
    elif role.is_error():
        await message.reply_text(role.error)