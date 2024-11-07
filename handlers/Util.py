from datetime import datetime, timedelta
import re
from time import sleep
from typing import List
from  import types
from Service import Chat, Command, Message, MutedUser, Role, RolePermission, User, UserChat


async def get_mentions(message: types.Message) -> List[types.User]:
    """Получает всех упомянутых пользователей в чате, кроме бота."""
    bot_username = (await message.bot.get_me()).username
    users = []
    # print(message.entities)
    for entity in message.entities or []:
        print(entity)
        if entity.type == "mention" and bot_username != entity.user.username:
            users.append(entity.user)
    return users

async def extract_datetime_from_message(message: types.Message):
    """Извлекает дату и/или время, указанные в сообщении, или возвращает время через 1 минуту, если ничего не указано."""
    current_date = datetime.now()

    datetime_patterns = [
        r"(\d{2})[./-](\d{2})[./-](\d{4})[ ]?(\d{2}:\d{2})?",  # дд.мм.гггг чч:мм или дд/мм/гггг чч:мм
        r"(\d{4})[./-](\d{2})[./-](\d{2})[ ]?(\d{2}:\d{2})?",  # гггг-мм-дд чч:мм
        r"(\d{2}:\d{2})"  # только время чч:мм
    ]
    
    for pattern in datetime_patterns:
        match = re.search(pattern, message.text)
        if match:
            date_str = match.group(0)
            try:
                # Если указана только дата (дд.мм.гггг или гггг-мм-дд)
                if re.match(r"^\d{2}[./-]\d{2}[./-]\d{4}$", date_str) or re.match(r"^\d{4}[./-]\d{2}[./-]\d{2}$", date_str):
                    date = datetime.strptime(date_str, "%d.%m.%Y" if '.' in date_str else "%Y-%m-%d")
                    date = date.replace(hour=0, minute=0)  # Устанавливаем время 00:00
                        
                # Если указано только время (чч:мм)
                elif re.match(r"^\d{2}:\d{2}$", date_str):
                    time = datetime.strptime(date_str, "%H:%M").time()
                    date = current_date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)
                
                # Если указаны дата и время
                else:
                    if len(date_str.split('-')[0]) == 4:  # гггг-мм-дд чч:мм
                        date_format = "%Y-%m-%d %H:%M"
                    else:  # дд.мм.гггг чч:мм или дд/мм/гггг чч:мм
                        date_format = "%d.%m.%Y %H:%M"
                    
                    date = datetime.strptime(date_str, date_format)
                
                return date
            except ValueError:
                continue
    # Если ни дата, ни время не указаны, возвращаем текущее время + 1 минута
    return current_date + timedelta(minutes=1)

async def mute_user(message: types.Message, chat_id, user_id, mute_end: datetime | timedelta):
    """Выдача мута"""
    await message.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False),
        until_date=mute_end
    )
    await sleep(mute_end)
    await message.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=types.ChatPermissions(can_send_messages=True, can_send_media_messages=True)
    )
    