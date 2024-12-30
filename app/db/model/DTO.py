from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator
import logging

from app.enum import UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
class UserDTO(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True

class UserChatDTO(BaseModel):
    user_id: int
    chat_id: int
    role: UserRole
    join_date: datetime
    
    class Config:
        from_attributes = True
    
class MessageDTO(BaseModel):
    id: Optional[int] = None
    message_id: int
    user_id: int
    chat_id: int
    message: str
    date: datetime
    
    class Config:
        from_attributes = True
    
class ChatDTO(BaseModel):
    id: int
    chat_name: str
    spam_mute_time: float
    spam_message: int
    spam_time: int
    delete_pattern: str
    
    class Config:
        from_attributes = True
    
class MutedUsersDTO(BaseModel):
    id: Optional[int] = None
    user_id: int
    chat_id: int
    time_end: datetime
    reason: str
        
    class Config:
        from_attributes = True

    
class BanUserDTO(BaseModel):
    id: Optional[int] = None
    user_id: int
    chat_id: int
    time_end: datetime
    reason: str
        
    class Config:
        from_attributes = True

model_config = ConfigDict(from_attributes=True)