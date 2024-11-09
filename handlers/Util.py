from datetime import datetime
import re
from typing import List
from telegram import Update, ChatPermissions, MessageEntity
from telegram.ext import ContextTypes
from dateutil import parser
from models.DTO import UserDTO
from service.UserService import UserService
                    
async def get_mentioned_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> List[UserDTO]:
    """Получает ID всех упомянутых пользователей по @username в чате, кроме бота."""
    bot_username = (await context.bot.get_me()).username
    mentioned_user = []
    
    if update.message and update.message.text:
        mentioned_usernames = re.findall(r'@(\w+)', update.message.text)
        for username in mentioned_usernames:
            if username.lower() != bot_username.lower():
                user = UserService().get_user_by_username(username)
                mentioned_user.append(user)
    return mentioned_user

async def extract_datetime_from_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Извлекает дату и/или время, указанные в сообщении."""
    current_date = datetime.now()

    datetime_patterns = [
        r"(\d{2})[./-](\d{2})[./-](\d{4})[ ]?(\d{2}:\d{2})?",  # дд.мм.гггг чч:мм или дд/мм/гггг чч:мм
        r"(\d{4})[./-](\d{2})[./-](\d{2})[ ]?(\d{2}:\d{2})?",  # гггг-мм-дд чч:мм
        r"(\d{2}[./:]\d{2})"  # только время чч:мм
    ]
    
    for pattern in datetime_patterns:
        match = re.search(pattern, update.message.text)
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
    return None

async def muted_user(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id, user_id, mute_end: datetime):
    """Выдача мута"""
    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(can_send_messages=False, can_send_media_messages=False),
        until_date=mute_end
    )
