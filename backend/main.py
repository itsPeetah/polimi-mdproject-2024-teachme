# stdlib imports
from os import getenv, system

# dependency imports
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

# custom imports
from lib.routes import *
from lib.auth import AuthenticationService
from lib.database import MongoDBConnector
from lib.log import Logger
from lib.llm import ChatbotManager

load_dotenv()

# services initialization

app = Flask(__name__)
CORS(app, origins="*")
app_db_connector = MongoDBConnector(getenv("MONGODB_URI"))
db = app_db_connector.connect("teachme_main")
user_auth = AuthenticationService(db)
logger = Logger(db)
chatbot_manager = ChatbotManager(5000)

# route registration

register_auth_routes(app, user_auth)
register_log_routes(app, db)
register_user_routes(app, db, logger)
register_conversation_routes(app, db, chatbot_manager, logger)

if __name__ == "__main__":
    chatbot_manager.start_heartbeat()
    system("python3 -m flask --app main run --debug --host 0.0.0.0 --port 5000")

    # from lib.llm import test_chatbot
    # test_chatbot(
    #     api_key=getenv("OPENAI_API_KEY"),
    #     conversation_id="6655f5096ace84de85540819",
    #     db=db,
    #     logger=logger
    # )
