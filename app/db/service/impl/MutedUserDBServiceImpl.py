from typing import Optional

from app.config.log_execution import log_class
from app.db.model.DTO import MutedUsersDTO
from app.db.model.Entity import MutedUser
from app.db.repository.baseImpl import MutedUserRepository
from app.db.service import MutedUserDBService

@log_class
class MutedUserDBServiceImpl(MutedUserDBService):
    def __init__(self, mute_repo: MutedUserRepository):
        self.repo = mute_repo

    def add_mute_user(self, mute_user: MutedUsersDTO) -> Optional[MutedUsersDTO]:
        if mute_user := self.repo.add(MutedUser(**mute_user.model_dump())):
            return MutedUsersDTO.model_validate(mute_user)
        return None

    def update_mute_user(self, mute_user: MutedUsersDTO) -> Optional[MutedUsersDTO]:
        if mute_user := self.repo.add(MutedUser(**mute_user.model_dump())):
            return MutedUsersDTO.model_validate(mute_user)
        return None

    def get_mute_user(self, chat_id: int, user_id: int) -> Optional[MutedUsersDTO]:
        if mute_user := self.repo.get_user_mute_by_chat_user(chat_id, user_id):
            return MutedUsersDTO.model_validate(mute_user)
        return None

    def get_active_mute_user(self, chat_id: int, user_id: int) -> Optional[MutedUsersDTO]:
        if mute_user := self.repo.get_active_user_mute_by_chat_user(chat_id, user_id):
            return MutedUsersDTO.model_validate(mute_user)
        return None