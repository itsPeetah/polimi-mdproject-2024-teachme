from ..database import Connector
from .log import Log

class Logger():
    def __init__(self, db_connector: Connector, db_name: str = "teachme_main"):
        self._db_connector = db_connector
        self._db_name = db_name

        db = self._db_connector.connect(self._db_name)
        self._logs = db.get_collection("logs")
    
    def log(self, log: Log):
        self._logs.insert_one(log_type = log.log_type, message = log.message, time_stamp = log.time_stamp)
