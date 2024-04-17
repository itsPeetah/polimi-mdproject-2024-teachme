from dataclasses import dataclass

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
