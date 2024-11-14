from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RoleDTO(BaseModel):
    id: Optional[int] = None
    role_name: str
    chat_id: int
    
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def log_mapping(cls, values):
        logger.info(f"Mapping values to RoleDTO: {values}")
        return values
    
class CommandDTO(BaseModel):
    id: Optional[int] = None
    command: str
    command_name: str
    description: str
    chat_id: int
    
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def log_mapping(cls, values):
        logger.info(f"Mapping values to CommandDTO: {values}")
        return values
    
class RolePermissionDTO(BaseModel):
    role_id: int
    command_id: int
    
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def log_mapping(cls, values):
        logger.info(f"Mapping values to RolePermissionDTO: {values}")
        return values
    
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
    join_date: datetime
    
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def log_mapping(cls, values):
        logger.info(f"Mapping values to UserChatDTO: {values}")
        return values
    
class MessageDTO(BaseModel):
    id: Optional[int] = None
    message_id: int
    user_id: int
    chat_id: int
    message: str
    date: datetime
    
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def log_mapping(cls, values):
        logger.info(f"Mapping values to MessageDTO: {values}")
        return values
    
class ChatDTO(BaseModel):
    id: int
    chat_name: str
    spam_mute_time: float
    spam_message: int
    spam_time: int
    delete_pattern: str
    
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def log_mapping(cls, values):
        logger.info(f"Mapping values to ChatDTO: {values}")
        return values
    
class MutedUsersDTO(BaseModel):
    id: Optional[int] = None
    user_id: int
    chat_id: int
    time_end: datetime
    reason: str
        
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def log_mapping(cls, values):
        logger.info(f"Mapping values to MutedUsersDTO: {values}")
        return values
    
class BanUserDTO(BaseModel):
    id: Optional[int] = None
    user_id: int
    chat_id: int
    time_end: datetime
    reason: str
        
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def log_mapping(cls, values):
        logger.info(f"Mapping values to BanUserDTO: {values}")
        return values
    
model_config = ConfigDict(from_attributes=True)