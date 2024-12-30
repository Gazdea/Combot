from typing import Optional

from app.config.log_execution import log_class
from app.db.repository.baseImpl import ChatRepository
from sqlalchemy.orm import Session
from app.db.model.Entity import Chat
from app.db.repository.impl import BaseRepositoryImpl

@log_class
class ChatRepositoryImpl(BaseRepositoryImpl[Chat], ChatRepository):
    def __init__(self, session: Session):
        super().__init__(Chat, session)
        self.session: Session = session
