"""
Module containing classes for managing databases and collections in MongoDB.
"""
# pylint: disable=line-too-long

from .Collection import Collection, CollectionDispatcher

class Database():
    """
    Represents a generic database.
    """
    def __init__(self) -> None:
        """
        Initialize a Database object.
        """
        pass

class MongoDB(Database):
    """
    Represents a MongoDB database.
    """
    def __init__(self, client, db_name: str = 'teachme_main') -> None:
        """
        Initialize a MongoDB object.

        :param client: the MongoDB client object
        :type client: any
        :param db_name: name of the database, defaults to 'teachme_main'
        :type db_name: str, optional
        :raises ConnectionError: if connection to the database fails
        """
        self._db_name = db_name
        self._client = client
        self._db = self._client[self._db_name]
        self._collection_dispatcher = CollectionDispatcher(collection_names=self._db.list_collection_names(), db=self._db)

        try:
            self._client.admin.command('ping')
        except Exception as exc:
            raise ConnectionError(f'Connection to the DB failed - {exc}') from exc

    def get_collection(self, collection_name: str):
        """
        Return the collection object for the given collection name.

        :param collection_name: name of the collection to be returned
        :type collection_name: str
        :return: the collection object
        :rtype: Collection
        """
        return self._collection_dispatcher.get_collection(collection_name)
    