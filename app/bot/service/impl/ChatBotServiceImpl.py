from typing import Dict, List, cast
from telegram import Update, Message
from telegram.ext import ContextTypes

from app.bot.service import ChatBotService
from app.db.model.DTO import UserChatDTO
from app.dto import BotResponse

class ChatBotServiceImpl(ChatBotService):
    def __init__(self) -> None:
        super().__init__()
    
    async def chat_user_join(self, update: Update, context: ContextTypes.DEFAULT_TYPE, users_chat: List[UserChatDTO]) -> BotResponse:
        return BotResponse(
            text = f"За сегодня приспоединилось к чату: {users_chat}"
            )
        
    async def chat_user_active(self, update: Update, context: ContextTypes.DEFAULT_TYPE, users: Dict[str, int]) -> BotResponse:
        response = ["Сбор информации о пользователях:"]
        for username, count_messages in users.items():
            response.append(f"Информация о {username}.\nЗа сегодня написал: {count_messages}")
            
        return BotResponse(
            text="\n".join(response)
            )
        
    async def chat_spam_mute_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> BotResponse:
        raise NotImplementedError()

    async def chat_spam_num_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> BotResponse:
        raise NotImplementedError()

    async def chat_spam_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> BotResponse:
        raise NotImplementedError()
    
    async def chat_delete_pattern(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> BotResponse:
        raise NotImplementedError()
