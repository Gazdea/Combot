from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RoleDTO(BaseModel):
    id: int
    role_name: str
    chat_id: int
    
    class Config:
        from_attributes = True

class CommandDTO(BaseModel):
    id: int
    command: str
    command_name: str
    description: str
    chat_id: int
    
    class Config:
        from_attributes = True

class RolePermissionDTO(BaseModel):
    role_id: int
    command_id: int
    
    class Config:
        from_attributes = True

class UserDTO(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def log_mapping(cls, values):
        logger.info(f"Mapping values to UserDTO: {values}")
        return values
    
class UserChatDTO(BaseModel):
    user_id: int
    chat_id: int
    role_id: int
    join_date: str
    
    class Config:
        from_attributes = True

class MessageDTO(BaseModel):
    id: Optional[int] = None
    message_id: int
    user_id: int
    chat_id: int
    message: str
    date: str
    
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
    user_id: int
    chat_id: int
    time_end: str
    reason: str
        
    class Config:
        from_attributes = True

class BanUserDTO(BaseModel):
    user_id: int
    chat_id: int
    time_end: str
    reason: str
        
    class Config:
        from_attributes = True

model_config = ConfigDict(from_attributes=True)