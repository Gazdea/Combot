from datetime import datetime
import re
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from app.db.model.DTO import BanUserDTO, MessageDTO, UserDTO, MutedUsersDTO
from app.di.ServiceDBContainer import ServiceDBContainer
from app.di.UtilContainer import UtilContainer

service_container = ServiceDBContainer
util_container = UtilContainer

async def user_mute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Заглушить пользователя."""
    # muted_user_service = service_container.muted_user_service()
    # bot_util = util_container.bot_util()
    
    # message = update.message
    # users = await bot_util.get_mentioned_users(update, context)
    # if not users:
    #     await message.reply_text('Необходимо указать пользователей, которых нужно заглушить. Пример @Username')
    #     return
    # mute_until = await bot_util.extract_datetime_from_message(update, context)
    # if not mute_until:
    #     await message.reply_text('Необходимо указать время заглушки. Пример 2001-01-01 или 01:01 или 1h, 1m, 1d, 1w или все вместе')
    #     return
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes:
    #     await message.reply_text('Необходимо указать причину заглушки. Пример \"Нам такой не нужен\"')
    #     return
    # for user in users:
    #     muted_user_service.add_mute_user(MutedUsersDTO(user_id=user.id, chat_id=message.chat.id, until_date=mute_until, reason=quotes[0]))
    #     await context.bot.restrict_chat_member(
    #         chat_id=message.chat.id,
    #         user_id=user.id,
    #         permissions=ChatPermissions.no_permissions(),
    #         until_date=mute_until
    #     )
    #     await message.reply_text(f'Пользователь {user.username} заглушен до {mute_until}')

async def user_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Снять мут с пользователя."""
    # muted_user_service = service_container.muted_user_service()
    # bot_util = util_container.bot_util()
    
    # message = update.message
    # users = await bot_util.get_mentioned_users(update, context)
    # if not users:
    #     await message.reply_text('Необходимо указать пользователей, с которых нужно снять мут. Пример @Username')
    #     return
    # for user in users:
    #     muted_user_service.update_mute_user(MutedUsersDTO(user_id=user.id, chat_id=message.chat.id, until_date=datetime.now()))
    #     await context.bot.restrict_chat_member(
    #         chat_id=message.chat.id,
    #         user_id=user.id,
    #         permissions=ChatPermissions.all_permissions(),
    #         until_date=datetime.now()
    #     )

async def user_kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выгнать пользователя из чата."""
    # banned_user_service = service_container.banned_user_service()
    # bot_util = util_container.bot_util()
    
    # message = update.message
    # users = await bot_util.get_mentioned_users(update, context)
    # if not users:
    #     await message.reply_text('Необходимо указать пользователей, которых нужно заглушить. Пример @Username')
    #     return
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes:
    #     await message.reply_text('Необходимо указать причину заглушки. Пример \"Нам такой не нужен\"')
    #     return
    # for user in users:
    #     banned_user_service.add_ban_user(BanUserDTO(user_id=user.id, chat_id=message.chat.id, until_date=datetime.now(), reason=quotes[0]))
    #     await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=user.id)
    #     await message.reply_text(f'Пользователь {user.username} выгнан из чата.')

async def user_ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Забанить пользователя."""
    # banned_user_service = service_container.banned_user_service()
    # bot_util = util_container.bot_util()
    
    # message = update.message
    # users = await bot_util.get_mentioned_users(update, context)
    # if not users:
    #     await message.reply_text('Необходимо указать пользователей, которых нужно заглушить. Пример @Username')
    #     return
    # mute_until = await bot_util.extract_datetime_from_message(update, context)
    # if not mute_until:
    #     await message.reply_text('Необходимо указать время заглушки. Пример 2001-01-01 или 01:01 или 1h, 1m, 1d, 1w или все вместе')
    #     return
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes:
    #     await message.reply_text('Необходимо указать причину заглушки. Пример \"Нам такой не нужен\"')
    #     return
    # for user in users:
    #     banned_user_service.add_ban_user(BanUserDTO(user_id=user.id, chat_id=message.chat.id, until_date=mute_until, reason=quotes[0]))
    #     await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=user.id, until_date=mute_until)
    #     await message.reply_text(f'Пользователь {user.username} забанен.')

async def user_unban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Разбанить пользователя."""
    # banned_user_service = service_container.banned_user_service()
    # bot_util = util_container.bot_util()
    
    # message = update.message
    # users = await bot_util.get_mentioned_users(update, context)
    # if not users:
    #     await message.reply_text('Необходимо указать пользователя, которого нужно разбанить. Пример @Username')
    #     return
    # for user in users:
    #     banned_user_service.update_ban_user(BanUserDTO(user_id=user.id, chat_id=message.chat.id, until_date=datetime.now()))
    #     await context.bot.unban_chat_member(chat_id=message.chat.id, user_id=user.id)
    #     await message.reply_text(f'Пользователь {user.username} разбанен.')

async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получает информацию о пользователе в чате."""
    # user_chat_service = service_container.user_chat_service()
    # role_service = service_container.role_service()
    # bot_util = util_container.bot_util()
    
    # message = update.message
    # users = await bot_util.get_mentioned_users(update, context)
    # for user in users:
    #     user_chat = user_chat_service.get_user_chat(message.chat.id, user.id)
    #     if user_chat.is_error():
    #         await message.reply_text(user_chat.error)
    #         return
    #     user_chat = user_chat.value
    #     role = role_service.get_role_by_chat_user(message.chat.id, user.id)
    #     if role.is_error():
    #         await message.reply_text(role.error)
    #         return
    #     role =role.value
    #     await message.reply_text(f"Информация о {user.username}.\nПрисоединился: {user_chat.join_date}\nРоль: {role.role_name}")

async def user_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Назначает роль пользователю."""
    # user_chat_service = service_container.user_chat_service()
    # bot_util = util_container.bot_util()
    
    # message = update.message
    # users = await bot_util.get_mentioned_users(update, context)
    # if not users:
    #     await message.reply_text('Необходимо указать пользователя. \"@username\"')
    #     return
    # quotes = await bot_util.get_quoted_text(update, context)
    # if not quotes:
    #     await message.reply_text('Необходимо указать роль. \"role\"')
    #     return
    # for user in users:
    #     user_chat_service.set_user_role(message.chat.id, user.id, quotes[0])
    # await message.reply_text("Роль назначена пользователю.")
