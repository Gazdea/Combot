from datetime import datetime
from typing import Optional
from models.Entity import BanUser
from .BaseRepository import BaseRepository
from config import session_scope

class BannedUserRepository(BaseRepository):
    def __init__(self):
        super().__init__(BanUser)
    
    def get_users_ban_by_chat(self, chat_id: int) -> list[BanUser]:
        with session_scope() as session:
            banned_users = session.query(BanUser).filter(BanUser.chat_id == chat_id).all()
            return banned_users
        
    def get_user_bans_by_chats(self, user_id: int) -> list[BanUser]:
        with session_scope() as session:
            banned_users = session.query(BanUser).filter(BanUser.user_id == user_id).all()
            return banned_users
        
    def get_user_ban_by_chat_user(self, chat_id: int, user_id: int, start_time: datetime, end_time: datetime) -> Optional[BanUser]:
        with session_scope() as session:
            banned_user = session.query(BanUser).filter(
                BanUser.chat_id == chat_id,
                BanUser.user_id == user_id,
                BanUser.time_end >= start_time,
                BanUser.time_end <= end_time
            ).first()
            return banned_user
