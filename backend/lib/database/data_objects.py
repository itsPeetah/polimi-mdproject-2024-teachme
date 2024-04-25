from dataclasses import dataclass
from typing import Optional


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
    ]  # ids for stuends this is teachers and for teachers this is students


# u1 = User(
#     "jajajajaja", "john", "234567", "john.doe@example.com", "student", ["asiasdugias"]
# )
# print(u1.__dict__)


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
