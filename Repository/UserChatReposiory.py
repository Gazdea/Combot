from datetime import date
from typing import Optional
from models.Entity import UserChat
from .BaseRepository import BaseRepository
from config import session_scope
from sqlalchemy.orm import make_transient

class UserChatRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserChat)
    
    def delete(self, chat_id: int, user_id: int) -> bool:
        with session_scope() as session:
            user_chat = session.query(UserChat).filter(UserChat.chat_id == chat_id, UserChat.user_id == user_id).first()
            if user_chat:
                session.delete(user_chat)
                return True
            return False
        
    def get_user_role(self, chat_id: int, user_id: int) -> Optional[UserChat]:
        with session_scope() as session:
            instance = session.query(UserChat).filter(
                UserChat.chat_id == chat_id, 
                UserChat.user_id == user_id
                ).first()
            session.expunge(instance)
            make_transient(instance)
            return instance
        

    def get_join_users(self, chat_id: int, date_start: date, date_end: date) -> list[UserChat]:
        with session_scope() as session:
            users = session.query(UserChat).filter(UserChat.chat_id == chat_id, UserChat.join_date >= date_start, UserChat.join_date <= date_end).all()
            for user in users:
                session.expunge(user)
                make_transient(user)
            return users