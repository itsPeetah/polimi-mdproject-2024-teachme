from dataclasses import dataclass
from datetime import datetime

from lib.log.log import LogType

@dataclass
class User:
    """
    Represents a user in the system.
    """
    id: int
    username: str
    password: str
    email: str
    role: str
    user_level: str

@dataclass
class Conversation:
    """
    Represents a conversation.
    """
    _id: any
    conversation_id: int
    user_level: str
    difficulty: str
    topic: str

@dataclass
class ChatMessage:
    """
    Represents a chat message.
    """
    message_id: int
    conversation_id: int
    sender_id: int
    message: str
    timestamp: int

@dataclass
class Log:
    """
    Represents a log message.
    """
    log_type: LogType
    message: str
    time_stamp: datetime
    
