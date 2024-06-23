"""
Module containing classes for connecting to MongoDB and managing the connection.
"""

# pylint: disable=line-too-long

from pymongo.mongo_client import MongoClient

from .Database import MongoDB


class Connector:
    """
    Represents a generic connector for connecting to a database.
    """

    def __init__(self, key: str = None) -> None:
        """
        Initialize a Connector object.

        Args:
            key (str, optional): Connection key.

        Raises:
            ConnectionError: If connection to the database fails.
        """
        pass

    def connect(self):
        """
        Connect to the database.
        """
        pass

    def close(self):
        """
        Close the database connection.
        """
        pass

    @property
    def connection_string(self):
        """
        Get the connection string.
        """
        pass


class MongoDBConnector(Connector):
    """
    Represents a connector for connecting to a MongoDB database.
    """

    def __init__(self, key: str = None) -> None:
        """
        Initialize a MongoDBConnector object.

        Args:
            key (str, optional): Connection key. Defaults to None.

        Raises:
            ConnectionError: If connection to the database fails.
        """
        self._key = key
        self._client = MongoClient(self._key)

        try:
            self._client.admin.command("ping")
        except Exception as exc:
            raise ConnectionError(f"Connection to the DB failed\n{exc}") from exc

    def connect(self, db_name: str = "teachme_main") -> MongoDB:
        """
        Connects to the MongoDB database.

        Args:
            db_name (str, optional): Name of the database. Defaults to 'teachme_main'.

        Returns:
            MongoDB: MongoDB object representing the connected database.
        """
        return MongoDB(self._client, db_name, connection_string=self._key)

    def close(self):
        self._client.close()

    @property
    def connection_string(self):
        return self._key


def main():
    """
    Main function to demonstrate MongoDB connection.
    """
    import dotenv
    import os

    dotenv.load_dotenv()
    key = os.getenv("MONGODB_URI")

    connector = MongoDBConnector(key)
    print("Connected to the DB")
    print(connector)
    print("Closing the connection")
    connector.close()
    print("Connection closed. Finishing...")


if __name__ == "__main__":
    main()
