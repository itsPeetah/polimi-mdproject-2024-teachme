from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from ..log import LogType


@dataclass
class User:
    """
    Represents a user in the system.
    """

    _id: str
    username: str
    password: str
    email: str
    role: str
    friends: list[
        str
    ]  # ids: for students this is teachers and for teachers this is students


@dataclass
class Conversation:
    """
    Represents a conversation.
    """

    _id: any
    user_level: str
    difficulty: str
    topic: str
    teacher_email: str
    student_email: str
    is_ended: bool
    time_limit: int
    parent_conversation_id: Optional[str]


@dataclass
class ChatMessage:
    """
    Represents a chat message.
    """

    message_id: any
    conversation_id: str
    sender_id: str
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


@dataclass
class ManagedConversation:
    """Represents an ended conversation."""

    _id: any
    messages: list
    role_reversed_prompt: str
    overall_feedback: str
