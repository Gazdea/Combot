from typing import Optional
from Models.Entity import User
from Repository.Base import BaseRepository
from config import session_scope

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_users(self, users_ids: list[int]) -> list[User]:
        with session_scope() as session:
            return session.query(User).filter(User.id.in_(users_ids)).all()