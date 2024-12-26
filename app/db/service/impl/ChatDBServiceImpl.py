from typing import Optional

from app.config.log_execution import log_class
from app.db.model.DTO import ChatDTO
from app.db.model.Entity import Chat
from app.db.repository.baseImpl import ChatRepository
from app.db.service import ChatDBService
from app.exception.businessExceptions import NotFoundChat

@log_class
class ChatDBServiceImpl(ChatDBService):
    
    def __init__(self, chat_repository: ChatRepository):
        self.repo = chat_repository

    def get_chat_by_id(self, chat_id: int) -> Optional[ChatDTO]:
        if chat := self.repo.get(chat_id):
            return ChatDTO.model_validate(chat)
        raise NotFoundChat

    def new_chat(self, chat_id: int, chat_name: str) -> Optional[ChatDTO]:
        if chat := self.repo.add_if_not_exists(
            Chat(**
                ChatDTO(
                    id=chat_id,
                    chat_name=chat_name,
                    spam_mute_time=60,
                    spam_message=10,
                    spam_time=10,
                    delete_pattern="http[s]?://\S+|www\.\S+"
                ).model_dump()
            )
        ):
            return ChatDTO.model_validate(chat)
        return None

    def update_chat(self, chat_dto: ChatDTO) -> Optional[ChatDTO]:
        if chat := self.repo.update(Chat(**chat_dto.model_dump())):
            return ChatDTO.model_validate(chat)
        raise NotFoundChat

    def update_spam_mute_time(self, chat_id: int, spam_mute_time: int) -> Optional[ChatDTO]:
        if chat := self.repo.get(chat_id):
            chat.spam_mute_time = spam_mute_time
            return ChatDTO.model_validate(self.repo.update(chat))
        raise NotFoundChat

    def update_spam_message(self, chat_id: int, spam_message: int) -> Optional[ChatDTO]:
        if chat := self.repo.get(chat_id):
            chat.spam_message = spam_message
            return ChatDTO.model_validate(self.repo.update(chat))
        raise NotFoundChat

    def update_spam_time(self, chat_id: int, spam_time: int) -> Optional[ChatDTO]:
        if chat := self.repo.get(chat_id):
            chat.spam_time = spam_time
            return ChatDTO.model_validate(self.repo.update(chat))
        raise NotFoundChat

    def update_delete_pattern(self, chat_id: int, delete_pattern: str) -> Optional[ChatDTO]:
        if chat := self.repo.get(chat_id):
            chat.delete_pattern = delete_pattern
            return ChatDTO.model_validate(self.repo.update(chat))