from datetime import date, datetime
from typing import Optional
from app.db.model.DTO import UserChatDTO
from app.db.model.Entity import UserChat
from app.db.repository.baseImpl import RoleRepository, UserChatRepository
from app.db.service import UserChatDBService

class UserChatDBServiceImpl(UserChatDBService):
    def __init__(self, user_chat_repo: UserChatRepository, role_repo: RoleRepository):
        self.role_repo = role_repo
        self.user_chat_repo = user_chat_repo

    def get_user_chat(self, chat_id: int, user_id: int) -> Optional[UserChatDTO]:
        if user_chat := self.user_chat_repo.get(chat_id=chat_id, user_id=user_id):
            return UserChatDTO.model_validate(user_chat)
        return None

    def get_stats_users_join(self, chat_id: int, date_start: date = date.today(), date_end: date = date.today()) -> Optional[list[UserChatDTO]]:
        if users := self.user_chat_repo.get_join_users(chat_id=chat_id, date_start=date_start, date_end=date_end):
            return [UserChatDTO.model_validate(user) for user in users]
        return None

    def set_user_role(self, chat_id: int, user_id: int, role_name: str) -> Optional[UserChatDTO]:
        if role := self.role_repo.get_role_by_role_name(chat_id, role_name):    
            if user_chat := self.user_chat_repo.get(chat_id, user_id):
                user_chat.role_id = role.id
                if user_chat := self.user_chat_repo.save(user_chat):
                    return UserChatDTO.model_validate(self.user_chat_repo.save(user_chat))
        return None

    def add_user_by_chat(self, user_id: int, chat_id: int, role_name: str, join_date: datetime) -> Optional[UserChatDTO]:
        if role := self.role_repo.get_role_by_role_name(chat_id, role_name):
            if user := self.user_chat_repo.save(UserChat(**UserChatDTO(
                                                            user_id=user_id,
                                                            chat_id=chat_id,
                                                            role_id=role.id,
                                                            join_date=join_date
                                                        ).model_dump())): 
                return UserChatDTO.model_validate(user)
        return None
        
    def delete_user_chat(self, chat_id: int, user_id: int) -> Optional[bool]:
        if user := self.user_chat_repo.delete(chat_id, user_id):
            return user
        return None