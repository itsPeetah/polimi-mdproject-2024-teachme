from pymongo.mongo_client import MongoClient

from .Database import MongoDB

class Connector():
    def __init__(self, key: str = None) -> None:
        pass
    
    def connect(self):
        pass
    
    def close(self):
        pass
    
    @property
    def connection_string(self):
        pass

class MongoDBConnector(Connector):
    def __init__(self, key: str = None) -> None:
        self._key = key
        self._client = MongoClient(self._key)
        
        try:
            self._client.admin.command('ping')
        except Exception as exc:
            raise Exception(f'Connection to the DB failed\n{exc}') from exc
    
    def connect(self, db_name: str = 'teachme_main') -> MongoDB:
        return MongoDB(self._client, db_name)

    def close(self):
        self._client.close()
        
    @property
    def connection_string(self):
        return self._key
    

def main():
    import dotenv
    import os
    
    dotenv.load_dotenv()
    key = os.getenv('MONGODB_URI')
    
    connector = MongoDBConnector(key)
    print("Connected to the DB")
    print(connector)
    print("Closing the connection")
    connector.close()
    print("Connection closed. Finishing...")

if __name__ == "__main__":
    main()