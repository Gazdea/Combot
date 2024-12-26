from datetime import date
from typing import List, Optional, Type

from app.config.log_execution import log_class
from app.db.model.Entity import UserChat
from sqlalchemy.orm import Session
from app.db.repository.baseImpl import UserChatRepository
from app.db.repository.impl import BaseRepositoryImpl
from sqlalchemy import between

@log_class
class UserChatRepositoryImpl(BaseRepositoryImpl[UserChat], UserChatRepository):
    def __init__(self, session: Session):
        super().__init__(UserChat, session)
        self.session: Session = session
    
    def delete(self, chat_id: int, user_id: int) -> bool:
        if (
            user_chat := self.session.query(UserChat)
            .filter(UserChat.chat_id == chat_id, UserChat.user_id == user_id)
            .first()
        ):
            self.session.delete(user_chat)
            self.session.commit()
            return True
        return False
        
    def get(self, chat_id: int, user_id: int) -> Optional[UserChat]:
        instance = self.session.query(UserChat).filter(
            UserChat.chat_id == chat_id, 
            UserChat.user_id == user_id
            ).first()
        return instance

    def get_join_users(self, chat_id: int, date_start: date, date_end: date) -> list[Type[UserChat]]:
        users = self.session.query(UserChat).filter(
            UserChat.chat_id == chat_id,
            between(UserChat.join_date,  date_start, date_end)
        ).all()
        return users

    def add_if_not_exists(self, instance: UserChat) -> Optional[UserChat]:
        if not self.session.query(UserChat).filter_by(chat_id=instance.chat_id, user_id=instance.user_id).first():
            self.session.add(instance)
            self.session.flush()
            self.session.commit()
            return instance