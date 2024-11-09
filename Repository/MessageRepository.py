from datetime import date
from typing import Optional
from models.Entity import Message
from .BaseRepository import BaseRepository
from config import session_scope

class MessageRepository(BaseRepository):
    def __init__(self):
        super().__init__(Message)

    def get_messages(self, chat_id: int, user_id: int) -> Optional[list[Message]]:
        with session_scope() as session:
            return session.query(Message).filter(Message.chat_id == chat_id, Message.user_id == user_id).all()

    def get_count_messages(self, chat_id: int, user_id: int, date_start: date, date_end: date) -> Optional[int]:
        with session_scope() as session:
            return session.query(Message).filter(
                Message.chat_id == chat_id, 
                Message.user_id == user_id, 
                Message.date >= date_start, 
                Message.date <= date_end
            ).count()