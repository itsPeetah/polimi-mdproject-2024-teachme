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

# ROUTES


@app.route("/create-friendship", methods=["POST"])
def create_friendship():
    data = request.get_json()
    teacher_email = data.get("teacher_email")
    student_email = data.get("student_email")
    # db = app_db_connector.connect("teachme_main")
    user_data_collection = db.get_collection("user_data")
    user_data_collection.create_friendship_using_email(
        teacher_email=teacher_email, student_email=student_email
    )  # TODO: add better error management
    return "Ok"


@app.route("/remove-friendship", methods=["POST"])
def remove_friendship():
    data = request.get_json()
    teacher_email = data.get("teacher_email")
    student_email = data.get("student_email")
    # db = app_db_connector.connect("teachme_main")
    user_data_collection = db.get_collection("user_data")
    user_data_collection.remove_friendship_using_email(
        teacher_email=teacher_email, student_email=student_email
    )  # TODO: add better error management
    return "Ok"


@app.route("/create-conversation", methods=["POST"])
def create_conversation():
    data = request.get_json()
    user_level = data.get("user_level")
    difficulty = data.get("difficulty")
    topic = data.get("topic")
    teacher_email = data.get("teacher_email")
    student_email = data.get("student_email")
    conversations_collection = db.get_collection("conversations")
    conversations_collection.create_conversation(
        user_level=user_level,
        difficulty=difficulty,
        topic=topic,
        teacher_email=teacher_email,
        student_email=student_email,
    )
    return "Ok"


@app.route("/get-friends/<user_email>", methods=["GET"])
def get_friends(user_email: str):
    # data = request.get_json()
    # user_email = data.get("user_email")
    # db = app_db_connector.connect("teachme_main")
    logger.log(
        Log(
            LogType.INFO,
            f"Received GET request at /get-friends/ for user_email: {user_email}",
        )
    )
    if user_email is None:
        return make_response(400, "KO")
    user_data_collection = db.get_collection("user_data")
    user_friends = user_data_collection.get_user_friends(user_email=user_email)
    return jsonify(user_friends)


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
