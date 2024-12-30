from datetime import datetime, timedelta
import re
from typing import List, Optional
from telegram import Update
from telegram.ext import ContextTypes
import pytz

async def get_mentioned_usernames(update: Update, context: ContextTypes.DEFAULT_TYPE) -> List[str]:
    """Получает username всех упомянутых пользователей по @username в чате, кроме бота."""
    bot_username = (await context.bot.get_me()).username
    mentioned_user = []
    if update.message and update.message.text:
        mentioned_usernames = re.findall(r'@(\w+)', update.message.text)
        for username in mentioned_usernames:
            if username.lower() != bot_username.lower():
                mentioned_user.append(username)
    return mentioned_user

async def get_quoted_text(update: Update) -> List[str]:
    """Returns a list of all text enclosed in double quotes"""
    text = update.message.text
    return [text.split('"')[i] for i in range(1, len(text.split('"')), 2)]

async def extract_datetime_from_message(update: Update) -> Optional[datetime] | None:
    """Извлекает дату и/или время, указанные в сообщении."""
    current_date = datetime.now(pytz.utc)
    datetime_patterns = [
        r"(\d{2})[./-](\d{2})[./-](\d{4})[ ]?(\d{2}:\d{2})?",  # дд.мм.гггг чч:мм или дд/мм/гггг чч:мм
        r"(\d{4})[./-](\d{2})[./-](\d{2})[ ]?(\d{2}:\d{2})?",  # гггг-мм-дд чч:мм
        r"(\d{2}[./:]\d{2})",  # только время чч:мм
    ]

    time_deltas = re.findall(r"([-+]?\d+)([hmdw])", update.message.text)
    for amount, unit in time_deltas:
        amount = int(amount)
        if unit == 'h':
            current_date += timedelta(hours=amount)
        elif unit == 'm':
            current_date += timedelta(minutes=amount)
        elif unit == 'd':
            current_date += timedelta(days=amount)
        elif unit == 'w':
            current_date += timedelta(weeks=amount)

    for pattern in datetime_patterns:
        if match := re.search(pattern, update.message.text):
            date_str = match[0]
            try:
                if (re.match(r"^\d{2}[./-]\d{2}[./-]\d{4}$", date_str)
                        or re.match(r"^\d{4}[./-]\d{2}[./-]\d{2}$", date_str)):
                    date = datetime.strptime(date_str, "%d.%m.%Y" if '.' in date_str else "%Y-%m-%d")
                    date = date.replace(hour=0, minute=0)

                elif re.match(r"^\d{2}:\d{2}$", date_str):
                    time = datetime.strptime(date_str, "%H:%M").time()
                    date = current_date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)

                elif len(date_str.split('-')[0]) == 4 or len(date_str.split('.')[0]) == 2:
                    date_format = "%Y-%m-%d %H:%M" if '-' in date_str else "%d.%m.%Y %H:%M"
                    date = datetime.strptime(date_str, date_format)

                return date
            except ValueError:
                continue

    return current_date if time_deltas else None
