from datetime import date
from typing import Optional
from Models.DTO import UserChatDTO
from Models.Entity import UserChat
from Repository.Base import BaseRepository
from config import session_scope

class UserChatRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserChat)

    def get_user_role(self, chat_id: int, user_id: int) -> Optional[UserChat]:
        with session_scope() as session:
            return UserChatDTO.model_validate(session.query(UserChat).filter(
                UserChat.chat_id == chat_id, 
                UserChat.user_id == user_id).first()
            )

    def get_join_users(self, chat_id: int, date_start: date, date_end: date) -> list[Optional[UserChat]]:
        with session_scope() as session:
            return [UserChatDTO.model_validate(user_chat for user_chat in session.query(UserChat).filter(UserChat.chat_id == chat_id, UserChat.join_date >= date_start, UserChat.join_date <= date_end).all)]
