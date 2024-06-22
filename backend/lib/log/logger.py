from ..database import Connector
from .log import Log

class Logger():
    def __init__(self, db):
        self._logs = db.get_collection("logs")
    
    def log(self, log: Log):
        """
        Logs a given log entry.

        Args:
            log (Log): The log entry to be logged.

        Returns:
            None
        """
        self._logs.insert_one(log_type=log.log_type, message=log.message, time_stamp=log.time_stamp)
