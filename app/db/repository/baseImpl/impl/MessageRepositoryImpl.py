from datetime import date
from typing import List, Optional
from app.db.model.Entity import Message
from app.db.repository.baseImpl import MessageRepository
from sqlalchemy.orm import Session
from app.db.repository.impl import BaseRepositoryImpl

class MessageRepositoryImpl(BaseRepositoryImpl[Message], MessageRepository):
    def __init__(self, session: Session):
        super().__init__(Message, session)
        self.session: Session = session

    def get_messages(self, chat_id: int, user_id: int) -> List[Message]:
        messages = self.session.query(Message).filter(Message.chat_id == chat_id, Message.user_id == user_id).all()
        return messages
        
    def get_count_messages(self, chat_id: int, user_id: int, date_start: date, date_end: date) -> Optional[int]:
        message = self.session.query(Message).filter(
            Message.chat_id == chat_id, 
            Message.user_id == user_id, 
            Message.date >= date_start, 
            Message.date <= date_end
        ).count()
        return message