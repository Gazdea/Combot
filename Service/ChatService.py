from typing import Optional
from models.DTO import ChatDTO
from models.Entity import Chat
from repository import ChatRepository

class ChatService:
    def __init__(self):
        self.repo = ChatRepository()
        
    def get_chat_by_id(self, chat_id: int) -> Optional[ChatDTO]:
        return ChatDTO.model_validate(self.repo.get(chat_id))

    def new_chat(self, chat_id: int, chat_name: str) -> Optional[ChatDTO]:
        return ChatDTO.model_validate(self.repo.save(
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
        )
    )
        
    def update_chat(self, chat_dto: ChatDTO) -> Optional[ChatDTO]:
        return ChatDTO.model_validate(self.repo.update(Chat(**chat_dto.model_dump())))