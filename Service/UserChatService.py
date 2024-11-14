from datetime import date, datetime
from typing import Optional
from models.DTO import UserChatDTO
from models.Entity import UserChat
from repository import RoleRepository, UserChatRepository

class UserChatService:
    def __init__(self):
        self.role_repo = RoleRepository()
        self.user_chat_repo = UserChatRepository()

    def get_user_chat(self, chat_id: int, user_id: int) -> Optional[UserChatDTO]:
        user_chat = self.user_chat_repo.get_user_role(chat_id=chat_id, user_id=user_id)
        return UserChatDTO.model_validate(user_chat) if user_chat else None

    def get_stats_users_join(self, chat_id: int, date_start: date = date.today(), date_end: date = date.today()) -> int:
        users = self.user_chat_repo.get_join_users(chat_id=chat_id, date_start=date_start, date_end=date_end)
        return [UserChatDTO.model_validate(user) for user in users]

    def set_user_role(self, chat_id: int, user_id: int, role_name: str) -> Optional[UserChatDTO]:
        role = self.role_repo.get_role_by_role_name(chat_id, role_name)
        user_chat = self.user_chat_repo.get_user_role(chat_id, user_id)
        if user_chat and role:
            user_chat.role_id = role.id
            return UserChatDTO.model_validate(self.user_chat_repo.update(user_chat))
        return None

    def add_user_by_chat(self, user_id: int, chat_id: int, role_name: str, join_date: datetime) -> Optional[UserChatDTO]:
        role = self.role_repo.get_role_by_role_name(chat_id, role_name)
        user_chat_dto = UserChatDTO(
            user_id=user_id,
            chat_id=chat_id,
            role_id=role.id,
            join_date=join_date
        )
        return UserChatDTO.model_validate(self.user_chat_repo.save(UserChat(**user_chat_dto.model_dump())))
    
    def delete_user_chat(self, chat_id: int, user_id: int) -> bool:
        return self.user_chat_repo.delete(chat_id, user_id)