"""
Module containing classes for managing collections in the database.
"""
# pylint: disable=line-too-long

from typing import List

from .data_objects import Conversation

class Collection():
    """
    Represents a generic collection in the database.
    """
    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a Collection object.

        :param collection: the collection object from the database
        :type collection: any
        :param collection_name: name of the collection
        :type collection_name: str
        """
        self._collection = collection
        self._collection_name = collection_name

    @property
    def collection_name(self):
        """
        Get the name of the collection.

        :return: the name of the collection
        :rtype: str
        """
        return self._collection_name

class ConversationsCollection(Collection):
    """
    Represents a collection of conversations in the database.
    
    Each conversation has the following fields:
    - conversation_id: int
    - user_level: str
    - difficulty: str
    - topic: str
    """
    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a ConversationsCollection object.

        :param collection: the collection object from the database
        :type collection: any
        :param collection_name: name of the collection
        :type collection_name: str
        """
        super().__init__(collection, collection_name)

    def find_by_id(self, conversation_id: int) -> Conversation:
        """
        Find a conversation by its ID.

        :param conversation_id: ID of the conversation to find
        :type conversation_id: int
        :return: the conversation object
        :rtype: Conversation
        """
        conversation_to_return = self._collection.find_one({"conversation_id": conversation_id})
        return Conversation(**conversation_to_return) if conversation_to_return is not None else None

    def insert_one(self, conversation_id: int, user_level: str = None, difficulty: str = None, topic: str = None):
        """
        Insert a new conversation into the collection.

        :param conversation_id: ID of the conversation
        :type conversation_id: int
        :param user_level: level of the user, defaults to None
        :type user_level: str, optional
        :param difficulty: difficulty of the conversation, defaults to None
        :type difficulty: str, optional
        :param topic: topic of the conversation, defaults to None
        :type topic: str, optional
        """
        conversation = {
            "conversation_id": conversation_id,
            "user_level": user_level,
            "difficulty": difficulty,
            "topic": topic,
        }
        self._collection.insert_one(conversation)

class UserDataCollection(Collection):
    """
    Represents a collection of user data in the database.
    """
    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a UserDataCollection object.

        :param collection: the collection object from the database
        :type collection: any
        :param collection_name: name of the collection
        :type collection_name: str
        """
        super().__init__(collection, collection_name)

class ChatMessageHistoryCollection(Collection):
    """
    Represents a collection of chat message history in the database.
    """
    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a ChatMessageHistoryCollection object.

        :param collection: the collection object from the database
        :type collection: any
        :param collection_name: name of the collection
        :type collection_name: str
        """
        super().__init__(collection, collection_name)

class CollectionDispatcher():
    """
    Dispatcher class for managing collections in the database.
    """
    def __init__(self, collection_names: List[str], db) -> None:
        """
        Initialize a CollectionDispatcher object.

        :param collection_names: list of collection names
        :type collection_names: List[str]
        :param db: the database object
        :type db: any
        """
        self._connection_names = collection_names
        self._db = db

    def get_collection(self, collection_name: str):
        """Return the collection object for the given collection name.

        :param collection_name: name of the collection to be returned
        :type collection_name: str
        :raises KeyError: if the collection name is not found in the database
        :return: the collection object
        :rtype: Collection
        """
        if collection_name not in self._connection_names:
            raise KeyError(f"Collection {collection_name} not found in the database.")

        # switching to the correct collection
        if collection_name=='conversations':
            return ConversationsCollection(self._db[collection_name], collection_name)
        elif collection_name=='user_data':
            return UserDataCollection(self._db[collection_name], collection_name)
        elif collection_name=='chat_message_history':
            return ChatMessageHistoryCollection(self._db[collection_name], collection_name)
        else:
            return Collection(self._db[collection_name], collection_name)