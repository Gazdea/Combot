from typing import List, Optional
from app.db.model.Entity import User
from sqlalchemy.orm import Session
from app.db.repository.baseImpl import UserRepository
from app.db.repository.impl import BaseRepositoryImpl

class UserRepositoryImpl(BaseRepositoryImpl[User], UserRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)
        self.session: Session = session

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(User.username == username).first()
        
    def get_users(self, users_ids: List[int]) -> List[User]:
        return self.session.query(User).filter(User.id.in_(users_ids)).all()