from typing import Optional
from models.DTO import UserDTO
from models.Entity import User
from repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        user = self.repo.get(user_id)
        return UserDTO.model_validate(user)

    def get_user_by_username(self, username: int) -> Optional[UserDTO]:
        user = self.repo.get_user_by_username(username)
        return UserDTO.model_validate(user)
    
    def add_user(self, user: UserDTO) -> Optional[UserDTO]:
        created_user = self.repo.save(User(**user.model_dump()))
        return UserDTO.model_validate(created_user)
