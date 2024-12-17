from abc import ABC, abstractmethod
from typing import List, Tuple
from telegram import Update
from telegram.ext import ContextTypes
from app.db.model.DTO import CommandDTO, UserDTO

class Util(ABC):

    @abstractmethod
    async def get_mentioned_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> List[UserDTO]:
        """Получает ID всех упомянутых пользователей по @username в чате, кроме бота."""
        raise NotImplementedError
        # bot_username = (await context.bot.get_me()).username
        # mentioned_user = []
        # if update.message and update.message.text:
        #     mentioned_usernames = re.findall(r'@(\w+)', update.message.text)
        #     for username in mentioned_usernames:
        #         if username.lower() != bot_username.lower():
        #             user = UserService().get_user_by_username(username)
        #             if user.is_success():
        #                 mentioned_user.append(user.value)
        #             else:
        #                 await update.message.reply_text(f'Пользователь {username} не зарегистрирован.')
        # return mentioned_user

    @abstractmethod
    async def get_quoted_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> List[str]:
        """Returns a list of all text enclosed in double quotes"""
        raise NotImplementedError
        # text = update.message.text
        # return [text.split('"')[i] for i in range(1, len(text.split('"')), 2)]

    @abstractmethod
    async def extract_datetime_from_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Извлекает дату и/или время, указанные в сообщении."""
        raise NotImplementedError
        # current_date = datetime.now()
        # datetime_patterns = [
        #     r"(\d{2})[./-](\d{2})[./-](\d{4})[ ]?(\d{2}:\d{2})?",  # дд.мм.гггг чч:мм или дд/мм/гггг чч:мм
        #     r"(\d{4})[./-](\d{2})[./-](\d{2})[ ]?(\d{2}:\d{2})?",  # гггг-мм-дд чч:мм
        #     r"(\d{2}[./:]\d{2})",  # только время чч:мм
        # ]

        # time_deltas = re.findall(r"(\d+)([hmdw])", update.message.text)
        # for amount, unit in time_deltas:
        #     amount = int(amount)
        #     if unit == 'h':
        #         current_date += timedelta(hours=amount)
        #     elif unit == 'm':
        #         current_date += timedelta(minutes=amount)
        #     elif unit == 'd':
        #         current_date += timedelta(days=amount)
        #     elif unit == 'w':
        #         current_date += timedelta(weeks=amount)

        # for pattern in datetime_patterns:
        #     if match := re.search(pattern, update.message.text):
        #         date_str = match[0]
        #         try:
        #             if re.match(r"^\d{2}[./-]\d{2}[./-]\d{4}$", date_str) or re.match(r"^\d{4}[./-]\d{2}[./-]\d{2}$", date_str):
        #                 date = datetime.strptime(date_str, "%d.%m.%Y" if '.' in date_str else "%Y-%m-%d")
        #                 date = date.replace(hour=0, minute=0)

        #             elif re.match(r"^\d{2}:\d{2}$", date_str):
        #                 time = datetime.strptime(date_str, "%H:%M").time()
        #                 date = current_date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)

        #             elif len(date_str.split('-')[0]) == 4 or len(date_str.split('.')[0]) == 2:
        #                 date_format = "%Y-%m-%d %H:%M" if '-' in date_str else "%d.%m.%Y %H:%M"
        #                 date = datetime.strptime(date_str, date_format)

        #             return date
        #         except ValueError:
        #             continue

        # return current_date if time_deltas else None

    @abstractmethod
    def check_methods(classes, chat_id: int, user_id: int) -> List[Tuple[CommandDTO, Tuple[str, str]]]:
        raise NotImplementedError
        # commands = CommandService().get_commands_by_chat_user(chat_id, user_id)
        # if commands.is_success():
        #     commands = commands.value
        #     implemented_methods = __find_methods(classes)
        #     implemented_methods_dict = {method[0]: method[1] for method in implemented_methods}
        #     return [
        #         (command, implemented_methods_dict.get(command.method_name, False))
        #         for command in commands
        #     ]

    @abstractmethod
    def method_search(classes, method_name: str) -> Tuple[str, str]:
        raise NotImplementedError
        # implemented_methods = __find_methods(classes)
        # for method in implemented_methods:
        #     if method[0] == method_name:
        #         return method
            
    @abstractmethod
    def __find_methods(classes) -> List[Tuple[str, str]]:
        raise NotImplementedError
        # implemented_methods = []
        # for cls in classes:
        #     for name in dir(cls):
        #         attr = getattr(cls, name)
        #         if inspect.isfunction(attr):
        #             docstring = attr.__doc__
        #             implemented_methods.append((name, docstring))
        # return implemented_methods