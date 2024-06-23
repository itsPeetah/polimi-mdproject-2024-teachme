"""
Module containing classes for managing databases and collections in MongoDB.
"""

# pylint: disable=line-too-long

from .Collection import Collection, CollectionDispatcher


class Database:
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

    def __init__(
        self, client, db_name: str = "teachme_main", connection_string: str = ""
    ) -> None:
        """
        Initialize a MongoDB object.

        Args:
            client (any): The MongoDB client object.
            db_name (str, optional): Name of the database. Defaults to 'teachme_main'.

        Raises:
            ConnectionError: If connection to the database fails.
        """
        self._db_name = db_name
        self._connection_string = connection_string
        self._client = client
        self._db = self._client[self._db_name]
        self._collection_dispatcher = CollectionDispatcher(
            collection_names=self._db.list_collection_names(), db=self._db
        )

        try:
            self._client.admin.command("ping")
        except Exception as exc:
            raise ConnectionError(f"Connection to the DB failed - {exc}") from exc

    @property
    def db_name(self):
        return self._db_name

    @property
    def db_connection_string(self):
        return self._connection_string

    def get_collection(self, collection_name: str):
        """
        Return the collection object for the given collection name.

        Args:
            collection_name (str): Name of the collection to be returned.

        Returns:
            Collection: The collection object.
        """
        return self._collection_dispatcher.get_collection(collection_name)
