from datetime import date
from typing import List, Optional, Any, Type

from sqlalchemy import Row, between, func

from app.config.log_execution import log_class
from app.db.model.Entity import Message
from app.db.repository.baseImpl import MessageRepository
from sqlalchemy.orm import Session
from app.db.repository.impl import BaseRepositoryImpl

@log_class
class MessageRepositoryImpl(BaseRepositoryImpl[Message], MessageRepository):
    def __init__(self, session: Session):
        super().__init__(Message, session)
        self.session: Session = session

    def get_messages(self, chat_id: int, user_id: int) -> list[Type[Message]]:
        messages = self.session.query(Message).filter(Message.chat_id == chat_id, Message.user_id == user_id).all()
        return messages
        
    def get_count_messages(self, chat_id: int, user_id: int, date_start: date, date_end: date) -> Optional[int]:
        message = self.session.query(Message).filter(
            Message.chat_id == chat_id, 
            Message.user_id == user_id, 
            between(Message.date, date_start, date_end)
        ).count()
        return message

    def get_top_users_by_message_count(self, chat_id: int, date_start: date, date_end: date) -> List[
        Row[tuple[Any, Any]]]:
        return self.session.query(
            Message.user_id,
            func.count(Message.id).label('message_count')
        ).filter(
            Message.chat_id == chat_id,
            between(Message.date, date_start, date_end)
        ).group_by(
            Message.user_id
        ).order_by(
            func.count(Message.id).desc()
        ).all()