from typing import Optional
from .BaseRepository import BaseRepository
from config import session_scope
from models.Entity import Chat

class ChatRepository(BaseRepository):
    def __init__(self):
        super().__init__(Chat)
