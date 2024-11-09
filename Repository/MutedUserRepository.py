from datetime import datetime
from typing import Optional
from models.Entity import MutedUser
from .BaseRepository import BaseRepository
from config import session_scope

class MutedUserRepository(BaseRepository):
    def __init__(self):
        super().__init__(MutedUser)
        
    def get_users_mute_by_chat(self, chat_id: int) -> Optional[list[MutedUser]]:
        with session_scope() as session:
            return session.query(MutedUser).filter(MutedUser.chat_id == chat_id).all()
        
    def get_user_mutes_by_chats(self, user_id: int) -> Optional[list[MutedUser]]:
        with session_scope() as session:
            return session.query(MutedUser).filter(MutedUser.user_id == user_id).all()
        
    def get_user_mute_by_chat_user(self, chat_id: int, user_id: int, start_time: datetime, end_time: datetime) -> Optional[MutedUser]:
        with session_scope() as session:
            return session.query(MutedUser).filter(
                MutedUser.chat_id == chat_id,
                MutedUser.user_id == user_id,
                MutedUser.time_end >= start_time,
                MutedUser.time_end <= end_time 
            ).first()