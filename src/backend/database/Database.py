from .Collection import Collection, CollectionDispatcher

class Database():
    def __init__(self) -> None:
        pass
    
class MongoDB(Database):
    def __init__(self, client, db_name: str = 'teachme_main') -> None:
        self._db_name = db_name
        self._client = client
        self._db = self._client[self._db_name]
        self._collection_dispatcher = CollectionDispatcher(collection_names=self._db.list_collection_names(), db=self._db)
        
        try:
            self._client.admin.command('ping')
        except Exception as exc:
            raise Exception(f'Connection to the DB failed - {exc}') from exc
    
    def get_collection(self, collection_name: str):
        return self._collection_dispatcher.get_collection(collection_name)
    