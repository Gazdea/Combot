from pydantic import BaseModel
from typing import List, Optional

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

class UserDTO(BaseModel):
    id: int
    username: str
    join_date: str

class UserChatDTO(BaseModel):
    user_id: int
    chat_id: int
    role_id: int

class MessageDTO(BaseModel):
    id: int
    user_id: int
    chat_id: int
    message: str
    message_type: str
    date: str

class ChatDTO(BaseModel):
    id: int
    chat_name: str
    roles: List[RoleDTO] = []
    commands: List[CommandDTO] = []
