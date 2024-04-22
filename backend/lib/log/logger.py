from lib.database.Connector import Connector
from lib.log.log import Log

import pymongo

class Logger():
    def __init__(self, mongo_client: pymongo.MongoClient, db_name: str = "teachme_main"):
        self.db_name = db_name

        self.db = mongo_client[self.db_name]
        self.logs = self.db["logs"]
    
    def log(self, log: Log):
        self.logs.insert_one({"log_type": log.log_type.value, "message": log.message, "timestamp": log.time_stamp})
