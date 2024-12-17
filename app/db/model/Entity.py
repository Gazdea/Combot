from pydantic import model_validator
from sqlalchemy import Float, Column, Integer, BigInteger, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship, DeclarativeBase

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(BigInteger, primary_key=True)
    chat_name = Column(Text)
    spam_mute_time = Column(Float, default=60)
    spam_message = Column(Integer, default=10)
    spam_time = Column(Integer, default=10)
    delete_pattern = Column(Text, default="http[s]?://\S+|www\.\S+")

    roles = relationship('Role', back_populates='chat')
    commands = relationship('Command', back_populates='chat')
    user_chats = relationship('UserChat', back_populates='chat')
    messages = relationship('Message', back_populates='chat')
    muted_users = relationship('MutedUser', back_populates='chat')
    ban_user = relationship('BanUser', back_populates='chat')

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(Text)
    chat_id = Column(BigInteger, ForeignKey('chats.id'))

    chat = relationship('Chat', back_populates='roles')
    permissions = relationship('RolePermission', back_populates='role')

class Command(Base):
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True)
    command = Column(Text)
    method_name = Column(Text)
    description = Column(Text)
    chat_id = Column(BigInteger, ForeignKey('chats.id'))

    chat = relationship('Chat', back_populates='commands')
    permissions = relationship('RolePermission', back_populates='command')

class RolePermission(Base):
    __tablename__ = 'role_permissions'

    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    command_id = Column(Integer, ForeignKey('commands.id'), primary_key=True)

    role = relationship('Role', back_populates='permissions')
    command = relationship('Command', back_populates='permissions')

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(Text)

    user_chats = relationship('UserChat', back_populates='user')
    muted_users = relationship('MutedUser', back_populates='user')
    ban_user = relationship('BanUser', back_populates='user')

class UserChat(Base):
    __tablename__ = 'user_chats'

    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    chat_id = Column(BigInteger, ForeignKey('chats.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    join_date = Column(TIMESTAMP, default=func.now())

    user = relationship('User', back_populates='user_chats')
    chat = relationship('Chat', back_populates='user_chats')
    role = relationship('Role')

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    chat_id = Column(BigInteger, ForeignKey('chats.id'))
    message = Column(Text)
    date = Column(TIMESTAMP)

    user = relationship('User')
    chat = relationship('Chat', back_populates='messages')

class MutedUser(Base):
    __tablename__ = 'muted_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    chat_id = Column(BigInteger, ForeignKey('chats.id'))
    time_end = Column(TIMESTAMP)
    reason = Column(Text)
    
    user = relationship('User', back_populates='muted_users')
    chat = relationship('Chat', back_populates='muted_users')

class BanUser(Base):
    __tablename__ = 'ban_users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    chat_id = Column(BigInteger, ForeignKey('chats.id'))
    time_end = Column(TIMESTAMP)
    reason = Column(Text)
    
    user = relationship('User', back_populates='ban_user')
    chat = relationship('Chat', back_populates='ban_user')