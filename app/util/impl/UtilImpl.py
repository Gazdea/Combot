from datetime import datetime, timedelta
import inspect
import re
from typing import List, Tuple
from sqlalchemy import null
from telegram import Update
from telegram.ext import ContextTypes
from app.bot.util import Util
from app.db.model.DTO import CommandDTO, UserDTO
from app.db.service import UserDBService, CommandDBService
from app.exception.businessExceptions import NotFoundUser
from app.exception.validationExceptions import ValidationMentionUser

class UtilImpl(Util):

    def __init__(self, user_service: UserDBService, command_service: CommandDBService):
        super().__init__()
        self.user_service = user_service
        self.command_service = command_service        
    
    async def get_mentioned_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> List[UserDTO]:
        """Получает ID всех упомянутых пользователей по @username в чате, кроме бота."""
        bot_username = (await context.bot.get_me()).username
        mentioned_user = []
        if update.message and update.message.text:
            mentioned_usernames = re.findall(r'@(\w+)', update.message.text)
            for username in mentioned_usernames:
                if username.lower() != bot_username.lower():
                    user = self.user_service.get_user_by_username(username)
                    if user != null:
                        mentioned_user.append(user)
                    else:
                        raise NotFoundUser(f'Пользователь {username} не зарегистрирован.')
        if not mentioned_user:
            raise ValidationMentionUser
        return mentioned_user

    async def get_quoted_text(self, update: Update) -> List[str]:
        """Returns a list of all text enclosed in double quotes"""
        text = update.message.text
        return [text.split('"')[i] for i in range(1, len(text.split('"')), 2)]

    async def extract_datetime_from_message(self, update: Update) -> datetime:
        """Извлекает дату и/или время, указанные в сообщении."""
        current_date = datetime.now()
        datetime_patterns = [
            r"(\d{2})[./-](\d{2})[./-](\d{4})[ ]?(\d{2}:\d{2})?",  # дд.мм.гггг чч:мм или дд/мм/гггг чч:мм
            r"(\d{4})[./-](\d{2})[./-](\d{2})[ ]?(\d{2}:\d{2})?",  # гггг-мм-дд чч:мм
            r"(\d{2}[./:]\d{2})",  # только время чч:мм
        ]

        time_deltas = re.findall(r"(\d+)([hmdw])", update.message.text)
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
                    if re.match(r"^\d{2}[./-]\d{2}[./-]\d{4}$", date_str) or re.match(r"^\d{4}[./-]\d{2}[./-]\d{2}$", date_str):
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

    def check_methods(self, classes, chat_id: int, user_id: int) -> List[Tuple[CommandDTO, Tuple[str, str]]]:
        commands = self.command_service.get_commands_by_chat_user(chat_id, user_id)
        if commands != null:
            implemented_methods = self.__find_methods(classes)
            implemented_methods_dict = {method[0]: method[1] for method in implemented_methods}
            return [
                (command, implemented_methods_dict.get(command.method_name, False))
                for command in commands
            ]

    def method_search(self, classes, method_name: str) -> Tuple[str, str]:
        implemented_methods = self.__find_methods(classes)
        for method in implemented_methods:
            if method[0] == method_name:
                return method
            
    def __find_methods(self, classes) -> List[Tuple[str, str]]:
        implemented_methods = []
        for cls in classes:
            for name in dir(cls):
                attr = getattr(cls, name)
                if inspect.isfunction(attr):
                    docstring = attr.__doc__
                    implemented_methods.append((name, docstring))
        return implemented_methods