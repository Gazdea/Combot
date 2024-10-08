from db.connection import add_chat_and_users, add_user
import time
from aiogram import types

from handlers import handler

class BotHandler:
    
    def __init__(self) -> None:
        self.spams = {}
        self.msgs = 4  # Количество сообщений
        self.max_time = 5  # Время в секундах
        self.ban_time = 10  # Время бана в секундах
    
    async def welcome_new_member(self, message: types.ChatMemberUpdated):
        for new_user in message.new_chat_members:
            if new_user.id == message.bot.id:
                chat_id = message.chat.id
                await message.bot.send_message(chat_id, "Бот добавлен в этот чат! Привет!")
                members = await message.bot.get_chat_administrators(chat_id)
                await add_chat_and_users(chat_id, [member.user for member in members])
            else:
                await add_user(new_user, message.chat.id)
                welcome_text = f"Привет, {new_user.first_name}! Добро пожаловать в наш чат."
                await message.bot.send_message(message.chat.id, welcome_text)
                
    async def is_spam(self, message: types.Message):
        current_time = int(time.time())
        user_id = message.from_user.id
        message.text = user_id
        if user_id in self.spams:
            usr = self.spams[user_id]
            if usr["banned"] > current_time:
                await handler.mute(message, self.ban_time)
                return True
            
            if usr["next_time"] > current_time:
                usr["messages"] += 1
                if usr["messages"] >= self.msgs:
                    usr["banned"] = current_time + self.ban_time
                    await handler.mute(message, self.ban_time)
                    return True
            else:
                usr["messages"] = 1
                usr["next_time"] = current_time + self.max_time
        else:
            self.spams[user_id] = {"next_time": current_time + self.max_time, "messages": 1, "banned": 0}
        
        return False
