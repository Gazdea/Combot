from datetime import date
from typing import Optional
from models.Entity import UserChat
from .BaseRepository import BaseRepository
from config import session_scope

class UserChatRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserChat)

    def save(self, user_chat: UserChat) -> Optional[UserChat]:
        with session_scope() as session:
            session.merge(user_chat)
            session.commit()
            return user_chat
        
    # def get(self, chat_id: int) -> Optional[UserChat]:
    #     with session_scope() as session:
    #         return session.query(UserChat).filter(UserChat.chat_id == chat_id).first()

    # def list(self) -> Optional[List[T]]:
    #     with session_scope() as session:
    #         return session.query(self.model).all()

    # def update(self, instance: T) -> Optional[T]:
    #     with session_scope() as session:
    #         session.merge(instance)
    #         session.commit()
    #         return instance

    # def delete(self, entity_id: int) -> Optional[bool]:
    #     with session_scope() as session:
    #         instance = session.query(self.model).filter(self.model.id == entity_id).first()
    #         if instance:
    #             session.delete(instance)
    #             session.commit()
    #             return True
    #         return False
        
    def get_user_role(self, chat_id: int, user_id: int) -> Optional[UserChat]:
        with session_scope() as session:
            return session.query(UserChat).filter(
                UserChat.chat_id == chat_id, 
                UserChat.user_id == user_id
                ).first()

    def get_join_users(self, chat_id: int, date_start: date, date_end: date) -> list[Optional[UserChat]]:
        with session_scope() as session:
            return session.query(UserChat).filter(UserChat.chat_id == chat_id, UserChat.join_date >= date_start, UserChat.join_date <= date_end).all()
