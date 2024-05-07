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

# execution

load_dotenv()

app = Flask(__name__)
CORS(app, origins="*")
app_db_connector = MongoDBConnector(
    getenv("MONGODB_URI")
)  # TEST if this works otherwise declare global client?
db = app_db_connector.connect("teachme_main")
user_auth = AuthenticationService(db)
logger = Logger(db)

register_auth_routes(app, user_auth)
register_log_routes(app, db)
register_user_routes(app, db, logger)
register_conversation_routes(app, db)

if __name__ == "__main__":
    system("python3 -m flask --app main run --debug")

    # from lib.llm import test_chatbot
    # test_chatbot(
    #     api_key=getenv("OPENAI_API_KEY"),
    #     conversation_id="6639ea3410a08c3689597981",
    #     db_connector=app_db_connector,
    #     db_name="teachme_main",
    #     logger = logger
    # )
