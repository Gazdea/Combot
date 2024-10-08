from aiogram import types

from handlers import handler

class BotHandler:
    
    async def welcome_new_member(self, message: types.ChatMemberUpdated):
        await handler.welcome_new_member(message)
                
    async def anti_spam_protection(self, message: types.Message, mute_time = 10, max_messages = 5, time_window = 5):
        await handler.anti_spam_protection(message, mute_time, max_messages, time_window)
    
    async def remove_links(self, message: types.Message):
        await handler.remove_links(message)