from typing import Optional, List

from app.config.log_execution import log_class
from app.db.model.DTO import UserDTO
from app.db.model.Entity import User
from app.db.repository.baseImpl import UserRepository
from app.db.service import UserDBService

@log_class
class UserDBServiceImpl(UserDBService):
    def __init__(self, user_repo: UserRepository):
        self.repo = user_repo

    def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        if user := self.repo.get(user_id):
            return UserDTO.model_validate(user)
        return None

    def get_user_by_username(self, username: str) -> Optional[UserDTO]:
        if user := self.repo.get_user_by_username(username):
            return UserDTO.model_validate(user)
        return None

    def get_users_by_usernames(self, usernames: List[str]) -> List[UserDTO]:
        users = self.repo.get_users_by_usernames(usernames)
        return [UserDTO.model_validate(user) for user in users]

    def add_user(self, user: UserDTO) -> Optional[UserDTO]:
        if created_user := self.repo.add_if_not_exists(User(**user.model_dump())):
            return UserDTO.model_validate(created_user)
        return None