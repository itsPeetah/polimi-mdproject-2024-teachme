import io
import struct
from os import getenv, system

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
    request,
)
from flask_cors import CORS
from lib.routes.conversationRoutes import register_conversation_routes
from lib.routes.userRoutes import register_user_routes
from lib.routes.logRoutes import register_log_routes
from lib.routes.authRoutes import register_auth_routes
from lib.auth import AuthenticationService
from lib.database import MongoDBConnector
from lib.llm import ConversationalChatBot, test_chatbot
from lib.log import Logger, LogType, Log

load_dotenv()

app = Flask(__name__)
CORS(app, origins="*")
EL_client = ElevenLabs(api_key=getenv("ELEVENLABS_API_KEY"))
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

    # user_auth.make_friends()
    # logger.log(Log(LogType.INFO, "Starting Flask app"))
    # conv_dict = user_auth.create_conversation()
    system("python3 -m flask --app main run --debug")
    # test_chatbot(
    #     api_key=getenv("OPENAI_API_KEY"),
    #     conversation_id="6639ea3410a08c3689597981",
    #     db_connector=app_db_connector,
    #     db_name="teachme_main",
    #     logger = logger
    # )
