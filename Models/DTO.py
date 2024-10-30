from typing import Optional
from pydantic import BaseModel, ConfigDict

class DTORole(BaseModel):
    id: int
    role_name: str
    chat_id: int

class DTOCommand(BaseModel):
    id: int
    command: str
    command_name: str
    description: str
    chat_id: int

class DTORolePermission(BaseModel):
    role_id: int
    command_id: int

class DTOUser(BaseModel):
    id: int
    username: str

class DTOUserChat(BaseModel):
    user_id: int
    chat_id: int
    role_id: int
    join_date: str

class DTOMessage(BaseModel):
    id: Optional[int] = None
    message_id: int
    user_id: int
    chat_id: int
    message: str
    message_type: str
    date: str

class DTOChat(BaseModel):
    id: int
    chat_name: str
    spam_mute_time: float
    spam_message: int
    spam_time: int
    delete_pattern: str

class DTOMutedUsers(BaseModel):
    user_id: int
    chat_id: int
    mute_end: str
    
model_config = ConfigDict(from_attributes=True)