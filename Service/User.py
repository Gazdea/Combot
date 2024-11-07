from typing import Optional
from Models.DTO import UserDTO
from Models.Entity import User
from Repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        user = self.repo.get(user_id)
        return UserDTO.model_validate(user)

    def add_user(self, user: UserDTO) -> Optional[UserDTO]:
        return UserDTO.model_validate((self.repo.create(User(**user.model_dump()))))
