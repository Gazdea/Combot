from typing import Dict, List
from telegram import Update
from telegram.ext import ContextTypes
from app.bot.service import ChatBotService
from app.db.service import ChatDBService
from app.db.model.DTO import UserChatDTO
from app.dto import BotResponse
from app.service import ChatLogicService
from app.util import Util

class ChatLogicServiceImpl(ChatLogicService):
    
    def __init__(self, chat_bot_service: ChatBotService, chat_db_service: ChatDBService, util: Util) -> None:
        super().__init__()
        self.chat_bot_service = chat_bot_service
        self.chat_db_service = chat_db_service
        self.util = util
    
    async def chat_user_join(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> BotResponse:
        
    
    async def chat_user_active(self, update: Update, context: ContextTypes.DEFAULT_TYPE, users: Dict[str, int]) -> None:
        raise NotImplementedError()

    async def chat_spam_mute_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()

    async def chat_spam_num_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()

    async def chat_spam_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()

    async def chat_delete_pattern(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError()
