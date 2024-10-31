from typing import Optional
from pydantic import BaseModel, ConfigDict

class RoleDTO(BaseModel):
    id: int
    role_name: str
    chat_id: int

class CommandDTO(BaseModel):
    id: int
    command: str
    command_name: str
    description: str
    chat_id: int

class RolePermissionDTO(BaseModel):
    role_id: int
    command_id: int

class UserDTO(BaseModel):
    id: int
    username: str

class UserChatDTO(BaseModel):
    user_id: int
    chat_id: int
    role_id: int
    join_date: str

class MessageDTO(BaseModel):
    id: Optional[int] = None
    message_id: int
    user_id: int
    chat_id: int
    message: str
    message_type: str
    date: str

class ChatDTO(BaseModel):
    id: int
    chat_name: str
    spam_mute_time: float
    spam_message: int
    spam_time: int
    delete_pattern: str

class MutedUsersDTO(BaseModel):
    user_id: int
    chat_id: int
    time_end: str
    reason: str
    
class BanUserDTO(BaseModel):
    user_id: int
    chat_id: int
    time_end: str
    reason: str
    
model_config = ConfigDict(from_attributes=True)