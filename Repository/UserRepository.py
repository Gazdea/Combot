from typing import Optional
from models.Entity import User
from .BaseRepository import BaseRepository
from config import session_scope
from sqlalchemy.orm import make_transient

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_username(self, username: str) -> Optional[User]:
        with session_scope() as session:
            user = session.query(User).filter(User.username == username).first()
            session.expunge(user)
            make_transient(user)
            return user
        
    def get_users(self, users_ids: list[int]) -> list[User]:
        with session_scope() as session:
            users = session.query(User).filter(User.id.in_(users_ids)).all()
            for user in users:
                session.expunge(user)
                make_transient(user)
            return user