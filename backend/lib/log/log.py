from datetime import datetime
from enum import Enum

class LogType(Enum):
    INFO = "INFO"
    ERROR = "ERROR"

class Log():
    def __init__(self, log_type: LogType, message: str):
        self.log_type = log_type
        self.message = message
        self.time_stamp = datetime.now()

    def __str__(self):
        return f"[{self.log_type.value}] [{self.time_stamp}] {self.message}"
