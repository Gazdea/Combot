from datetime import datetime
from typing import List, Optional

from app.config.log_execution import log_class
from app.db.model.Entity import BanUser
from app.db.repository.baseImpl import BannedUserRepository
from sqlalchemy.orm import Session
from app.db.repository.impl import BaseRepositoryImpl

@log_class
class BannedUserRepositoryImpl(BaseRepositoryImpl[BanUser], BannedUserRepository):
    def __init__(self, session: Session):
        super().__init__(BanUser, session)
        self.session: Session = session
    
    def get_users_ban_by_chat(self, chat_id: int) -> List[BanUser]:
        banned_users = self.session.query(BanUser).filter(BanUser.chat_id == chat_id).all()
        return banned_users
        
    def get_user_bans_by_chats(self, user_id: int) -> List[BanUser]:
            banned_users = self.session.query(BanUser).filter(BanUser.user_id == user_id).all()
            return banned_users
        
    def get_user_ban_by_chat_user(self, chat_id: int, user_id: int, start_time: datetime, end_time: datetime) -> Optional[BanUser]:
            banned_user = self.session.query(BanUser).filter(
                BanUser.chat_id == chat_id,
                BanUser.user_id == user_id,
                BanUser.time_end >= start_time,
                BanUser.time_end <= end_time
            ).first()
            return banned_user
