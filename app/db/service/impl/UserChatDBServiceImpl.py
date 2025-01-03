from datetime import date, datetime, timedelta
from typing import Optional

from app.config.log_execution import log_class
from app.db.model.DTO import UserChatDTO
from app.db.model.Entity import UserChat
from app.db.repository.baseImpl import UserChatRepository
from app.db.service import UserChatDBService
from app.enum import UserRole
from app.exception.businessExceptions import NotFoundUser

@log_class
class UserChatDBServiceImpl(UserChatDBService):
    def __init__(self, user_chat_repo: UserChatRepository):
        self.user_chat_repo = user_chat_repo

    def get_user_chat(self, chat_id: int, user_id: int) -> Optional[UserChatDTO]:
        if user_chat := self.user_chat_repo.get(chat_id=chat_id, user_id=user_id):
            return UserChatDTO.model_validate(user_chat)
        raise NotFoundUser

    def get_stats_users_join(self, chat_id: int, date_start: date = date.today(), date_end: date = date.today() +  timedelta(days=1)) -> Optional[list[UserChatDTO]]:
        if users := self.user_chat_repo.get_join_users(chat_id=chat_id, date_start=date_start, date_end=date_end):
            return [UserChatDTO.model_validate(user) for user in users]
        return None

    def set_user_role(self, chat_id: int, user_id: int, role: UserRole) -> Optional[UserChatDTO]:
        if user_chat := self.user_chat_repo.get(chat_id, user_id):
            user_chat.role = role
            if user_chat := self.user_chat_repo.add(user_chat):
                return UserChatDTO.model_validate(self.user_chat_repo.update(user_chat))
        return None

    def add_user_by_chat(self, user_id: int, chat_id: int, role: UserRole, join_date: datetime) -> Optional[UserChatDTO]:
        if user := self.user_chat_repo.add_if_not_exists(UserChat(**UserChatDTO(
                                                        user_id=user_id,
                                                        chat_id=chat_id,
                                                        role=role,
                                                        join_date=join_date
                                                    ).model_dump())):
            return UserChatDTO.model_validate(user)
        return None

    def delete_user_chat(self, chat_id: int, user_id: int) -> Optional[bool]:
        if user := self.user_chat_repo.delete(chat_id, user_id):
            return user
        return None