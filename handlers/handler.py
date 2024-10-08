from abc import ABC, abstractmethod
import asyncio
from db.connection import get_user_id
import time
from aiogram import types

class Handler(ABC):
    
    async def start(self, message):
        await noRule(message)
        pass
    
    async def help(self, message):
        await noRule(message)
        pass
    
    async def mute(self, message):
        await noRule(message)
        pass
    
    async def unmute(self, message):
        await noRule(message)
        pass
    
    async def ban(self, message):
        await noRule(message)
        pass

    async def unban(self, message):
        await noRule(message)
        pass

    async def kick(self, message):
        await noRule(message)
        pass

    async def delete_message(self, message):
        await noRule(message)
        pass

    async def info(self, message: types.Message):
        """Вывод информации о боте для админа."""
        bot_info = """
Этот бот позволяет модерировать чат.
Разработан для упрощения администрирования.
Создатель @Gazdea
        """
        await message.answer(bot_info)

async def noRule(message : types.Message):
    await message.answer("У вас нет прав.")
    pass

async def _get_user_id_from_message(message: types.Message):
    """Получить ID пользователя из сообщения."""
    user_id = None

    # 1. Если это ответ на сообщение
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    
    # 2. Если это упоминание (например, @username)
    elif message.entities:
        for entity in message.entities:
            if entity.type == 'mention':
                username = message.text[entity.offset:entity.offset + entity.length].lstrip('@')
                try:
                    user_id = await get_user_id(username)
                except Exception as e:
                    print(f"Ошибка при получении пользователя по имени: {e}")
    
    # 3. Если ID передан прямо в сообщении
    else:
        try:
            user_id = int(message.text)
        except ValueError:
            pass

    return user_id


async def _get_message_id_from_message(message: types.Message):
    """Получить ID сообщения, на которое ответили"""
    if message.reply_to_message:
        return message.reply_to_message.message_id
    return None


async def delete_message(message: types.Message):
    """Удаляет сообщение из чата"""
    message_id = await _get_message_id_from_message(message)
    if message_id:
        try:
            await message.bot.delete_message(message.chat.id, message_id)
            await message.bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            await message.answer(f"Ошибка при удалении: {e}")


async def kick(message: types.Message):
    """Выгнать пользователя из чата"""
    user_id = await _get_user_id_from_message(message)
    if user_id:
        try:
            await message.bot.kick_chat_member(message.chat.id, user_id)
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.answer("Пользователь был выгнан.")
        except Exception as e:
            await message.answer(f"Ошибка при выгоне: {e}")
    else:
        await message.answer("Ответьте на сообщение пользователя, которого хотите выгнать, или укажите @username.")


async def mute(message: types.Message, mute_time=3600):
    """Заглушить пользователя"""
    user_id = await _get_user_id_from_message(message)
    if user_id:
        try:
            current_time = int(time.time())
            until_time = current_time + mute_time

            await message.bot.restrict_chat_member(
                message.chat.id, 
                user_id, 
                until_date=until_time, 
                permissions=types.ChatPermissions(can_send_messages=False)
            )
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.answer(f"Пользователь заглушен на {mute_time / 60:.1f} мин.")
            
            await asyncio.sleep(mute_time)
            # Снятие ограничения автоматически по истечении времени
            await message.bot.restrict_chat_member(
                message.chat.id, 
                user_id, 
                permissions=types.ChatPermissions(can_send_messages=True)
            )
            await message.answer("Пользователь размьючен.")
            
        except Exception as e:
            await message.answer(f"Ошибка при мутации: {e}")
    else:
        await message.answer("Ответьте на сообщение пользователя, которого хотите заглушить.")


async def unmute(message: types.Message):
    """Снять мут с пользователя"""
    user_id = await _get_user_id_from_message(message)
    if user_id:
        try:
            await message.bot.restrict_chat_member(message.chat.id, user_id, permissions=types.ChatPermissions(can_send_messages=True))
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.answer("Мут снят.")
        except Exception as e:
            await message.answer(f"Ошибка при снятии мута: {e}")
    else:
        await message.answer("Ответьте на сообщение пользователя, с которого хотите снять мут.")


async def ban(message: types.Message):
    """Забанить пользователя"""
    user_id = await _get_user_id_from_message(message)
    if user_id:
        try:
            await message.bot.ban_chat_member(message.chat.id, user_id)
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.answer("Пользователь забанен.")
        except Exception as e:
            await message.answer(f"Ошибка при бане: {e}")
    else:
        await message.answer("Ответьте на сообщение пользователя, которого хотите забанить.")


async def unban(message: types.Message):
    """Разбанить пользователя"""
    user_id = await _get_user_id_from_message(message)
    if user_id:
        try:
            await message.bot.unban_chat_member(message.chat.id, user_id)
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.answer("Пользователь разбанен.")
        except Exception as e:
            await message.answer(f"Ошибка при разбане: {e}")
    else:
        await message.answer("Ответьте на сообщение пользователя, которого хотите разбанить.")
