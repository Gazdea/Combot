from models.DTO import MutedUsersDTO
from repository import MutedUserRepository

class MutedUserService:
    def __init__(self):
        self.repo = MutedUserRepository()
        
    def get_mute_user(self, user_id: int, chat_id: int) -> MutedUsersDTO:
        return MutedUsersDTO.model_validate(self.repo.get_user_mute_by_chat_user(chat_id, user_id))
