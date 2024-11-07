from typing import Optional
from Repository.Base import BaseRepository
from config import session_scope
from Models.Entity import Chat

class ChatRepository(BaseRepository):
    def __init__(self):
        super().__init__(Chat)
