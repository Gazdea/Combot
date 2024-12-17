from typing import Optional
from app.db.model.DTO import ChatDTO
from abc import ABC, abstractmethod

class ChatDBService(ABC):
        
    @abstractmethod
    def get_chat_by_id(self, chat_id: int) -> Optional[ChatDTO]:
        pass
    
    @abstractmethod
    def new_chat(self, chat_id: int, chat_name: str) -> Optional[ChatDTO]:
        pass
        
    @abstractmethod
    def update_chat(self, chat_dto: ChatDTO) -> Optional[ChatDTO]:
        pass