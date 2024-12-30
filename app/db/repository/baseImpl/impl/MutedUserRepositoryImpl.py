from datetime import datetime
from typing import List, Optional
from app.config.log_execution import log_class
from app.db.model.Entity import MutedUser
from app.db.repository.baseImpl import MutedUserRepository
from sqlalchemy.orm import Session
from app.db.repository.impl import BaseRepositoryImpl
import pytz

@log_class
class MutedUserRepositoryImpl(BaseRepositoryImpl[MutedUser], MutedUserRepository):
    def __init__(self, session: Session):
        super().__init__(MutedUser, session)
        self.session: Session = session
        
    def get_users_mute_by_chat(self, chat_id: int) -> List[MutedUser]:
            mutes = self.session.query(MutedUser).filter(MutedUser.chat_id == chat_id).all()
            return mutes
        
    def get_user_mutes_by_chats(self, user_id: int) -> List[MutedUser]:
            mutes = self.session.query(MutedUser).filter(MutedUser.user_id == user_id).all()
            return mutes
        
    def get_user_mute_by_chat_user(self, chat_id: int, user_id: int, start_time: datetime, end_time: datetime) -> Optional[MutedUser]:
            mute = self.session.query(MutedUser).filter(
                MutedUser.chat_id == chat_id,
                MutedUser.user_id == user_id,
                MutedUser.time_end >= start_time,
                MutedUser.time_end <= end_time 
            ).first()
            return mute

    def get_active_user_mute_by_chat_user(self, chat_id: int, user_id: int) -> Optional[MutedUser]:
            mute = (self.session.query(MutedUser).filter(
                MutedUser.chat_id == chat_id,
                MutedUser.user_id == user_id,
                MutedUser.time_end > datetime.now(pytz.utc),
            )
            .order_by(MutedUser.id.desc())
            .first())
            return mute