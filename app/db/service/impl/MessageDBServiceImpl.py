from datetime import date, timedelta
from typing import Dict, List, Optional

from app.config.log_execution import log_class
from app.db.model.Entity import Message
from app.db.repository.baseImpl import MessageRepository
from app.db.model.DTO import MessageDTO
from app.db.service import MessageDBService
from app.exception.businessExceptions import NotFound

@log_class
class MessageDBServiceImpl(MessageDBService):
    def __init__(self, msg_repo: MessageRepository):
        self.repo = msg_repo

    def get_stat_user_message(self, chat_id: int, user_id: int, date_start: date = date.today(), date_end: date = date.today() + timedelta(days=1)) -> Optional[int]:
        if message := self.repo.get_count_messages(chat_id, user_id, date_start, date_end):
            return message
        raise NotFound

    def get_stats_users_message(self, chat_id: int, users_ids: List[int], date_start: date = date.today(), date_end: date = date.today() + timedelta(days=1)) -> List[Dict[int, int]]:
        user_messages = []
        for user_id in users_ids:
            message_count = self.repo.get_count_messages(chat_id, user_id, date_start, date_end)
            if message_count:
                user_messages.append({"user_id": user_id, "message_count": message_count})
        return user_messages

    def get_messages_by_chat_user(self, chat_id: int, user_id: int) -> Optional[list[MessageDTO]]:
        if messages := self.repo.get_messages(chat_id, user_id):
            return [MessageDTO.model_validate(message) for message in messages]
        raise NotFound

    def save_message(self, message: MessageDTO) -> Optional[MessageDTO]:
        if create_message := self.repo.save(Message(**message.model_dump())):
            return MessageDTO.model_validate(create_message)
        raise NotFound
