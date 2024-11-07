from datetime import date
from typing import List
from Models.Entity import Message
from Repository import MessageRepository
from Models.DTO import MessageDTO

class MessageService:
    def __init__(self):
        self.repo = MessageRepository()

    def get_stat_user_message(self, chat_id: int, user_id: int, date_start: date = date.today(), date_end: date = date.today()) -> int:
        return self.repo.get_count_messages(chat_id, user_id, date_start, date_end)

    def get_messages_by_chat_user(self, chat_id: int, user_id: int) -> List[MessageDTO]:
        messages = self.repo.get_messages(chat_id, user_id)
        return [MessageDTO.model_validate(message) for message in messages]

    def save_message(self, message: MessageDTO) -> MessageDTO:
        return MessageDTO.model_validate(self.repo.create(Message(**message.model_dump())))
