from pydantic import BaseModel
from typing import List, Optional

class Role(BaseModel):
    id: int
    role_name: str
    chat_id: int

class Command(BaseModel):
    id: int
    command: str
    command_name: str
    description: str
    chat_id: int

class RolePermission(BaseModel):
    role_id: int
    command_id: int

class User(BaseModel):
    id: int
    username: str

class UserChat(BaseModel):
    user_id: int
    chat_id: int
    role_id: int
    join_date: str

class Message(BaseModel):
    id: int
    user_id: int
    chat_id: int
    message: str
    message_type: str
    date: str

class Chat(BaseModel):
    id: int
    chat_name: str
