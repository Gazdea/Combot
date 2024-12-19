from telegram import Update, ChatMemberAdministrator, ChatMemberOwner
from telegram.ext import ContextTypes
from app.bot.handler import Debug
from app.bot.util import Util
from app.db.service import ChatDBService
from app.controller import all_controller

class DebugImpl(Debug):
    
    def __init__(self, chat_service: ChatDBService, util: Util):
        super().__init__()
        self.chat_service = chat_service
        self.util = util
      
    async def debug(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Проверка работоспособности бота и подключений."""
        message = update.message
        response = ["Запускаю проверку системы..."]

        # Проверка подключения к API Telegram
        try:
            bot_info = await context.bot.get_me()
            response.append(f"Подключение к API Telegram успешно.\nИмя бота: {bot_info.first_name}\nUsername: @{bot_info.username}")
        except Exception as e:
            response.append(f"Ошибка подключения к API Telegram: {str(e)}")
            await message.reply_text("\n".join(response))
            return

        # Проверка административных прав бота в чате
        try:
            chat_member = await context.bot.get_chat_member(message.chat.id, context.bot.id)
            if isinstance(chat_member, (ChatMemberAdministrator, ChatMemberOwner)):
                response.append("У бота есть административные права в этом чате.")
            else:
                response.append("У бота нет административных прав в этом чате.")
        except Exception as e:
            response.append(f"Ошибка проверки прав администратора: {str(e)}")

        # Проверка подключения к базе данных
        try:
            chat_info = self.chat_service.get_chat_by_id(message.chat.id)
            if chat_info:
                response.append("Подключение к базе данных успешно. Чат найден в базе данных.")
            else:
                response.append("Чат не найден в базе данных. Создаю запись.")
                self.chat_service.new_chat(message.chat.id, message.chat.title)
        except Exception as e:
            response.append(f"Ошибка подключения к базе данных: {str(e)}")

        # Проверка: является ли сообщение ответом на другое сообщение
        if message.reply_to_message:
            response.append("Это сообщение является ответом на другое сообщение.")
        else:
            response.append("Нет ответа на сообщение.")

        # Получение упомянутых пользователей, кроме бота
        users = await self.util.get_mentioned_users(update, context)
        if users:
            response.append(f"Упомянутые пользователи (кроме бота): {', '.join([str(f'{user.id} {user.username}' ) for user in users])}")
        else:
            response.append("Нет упомянутых пользователей (кроме бота).")

        # Извлечение даты и времени из сообщения
        extracted_date = await self.util.extract_datetime_from_message(update)
        if extracted_date:
            response.append(f"Извлечённая дата и время: {extracted_date.strftime('%d.%m.%Y %H:%M')}")
        else:
            response.append("Дата и время не указаны или не распознаны.")

        quotes = await self.util.get_quoted_text(update)
        # Извлечение вложенного текста в ""
        if quotes:
            response.append(f"Извлеченные данные из ковычек {quotes}")
        else:
            response.append("Извлеченных данных нету")

        # Проверка готовности методов
        if quotes and quotes[0] == "method":
            if len(quotes) == 1:
                ready_methods = self.util.check_methods(all_controller, message.chat.id, message.from_user.id)
                methods = [f"{method[0].command} => {method[0].method_name}\n- {method[1]}" for method in ready_methods]
                response.append("\n".join(methods))
                
            elif len(quotes) == 2 and (method := self.util.method_search(all_controller, message.chat.id, message.from_user.id, quotes[1])):
                method = f"{method[0]}\n- {method[1]}"
                response.append(method)
            
            else:
                response.append("Неизвестная команда")
                
        else:
            response.append("Методы не проверены. Для проверки напишите \"method\" или \"method \" \"имя command\"")

        # Отправка собранного сообщения
        response.append("Проверка завершена успешно.")
        await message.reply_text("\n".join(response))
        
