from typing import List

class Collection():
    def __init__(self, collection, collection_name: str) -> None:
        self._collection = collection
        self._collection_name = collection_name
        
    @property
    def collection_name(self):
        return self._collection_name
    
class ConversationsCollection(Collection):
    def __init__(self, collection, collection_name: str) -> None:
        super().__init__(collection, collection_name)
        
    def find_by_id(self, conversation_id: int):
        return self._collection.find_one({"conversation_id": conversation_id})
    
    def insert_one(self, conversation_id: int, user_level: str = None, difficulty: str = None, topic: str = None):
        conversation = {
            "conversation_id": conversation_id,
            "user_level": user_level,
            "difficulty": difficulty,
            "topic": topic,
        }
        self._collection.insert_one(conversation)

class UserDataCollection(Collection):
    def __init__(self, collection, collection_name: str) -> None:
        super().__init__(collection, collection_name)

class ChatMessageHistoryCollection(Collection):
    def __init__(self, collection, collection_name: str) -> None:
        super().__init__(collection, collection_name)
        
class CollectionDispatcher():
    def __init__(self, collection_names: List[str], db) -> None:
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
