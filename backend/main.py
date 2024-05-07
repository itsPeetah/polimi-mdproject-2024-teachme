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

audio_buffer_handlers = {}

register_auth_routes(app, user_auth)
register_log_routes(app, db)

# ROUTES


@app.route("/text-to-speech", methods=["GET"])
def text_to_speech():
    text = request.args.get("text")
    audio_tts = EL_client.generate(text=text)
    response = Response(audio_tts, mimetype="audio/wav")
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response


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


def get_chatbot_answer(prompt: str) -> str:
    chatbot = ConversationalChatBot(
        api_key=getenv("OPENAI_API_KEY"),
        conversation_id=1,
        db_connector=app_db_connector,
        logger=logger,
    )
    response = chatbot.send_message(prompt).content
    return response


def load_audio(
    audio_file,
):  # TODO: DEPRECATED TO ADJUST WITH NEW LOGIC (useless, could be removed)
    # Getting the audio file parameters
    # Read the header to get audio file information
    audio_file = io.BytesIO(audio_file)
    header = audio_file.read(
        44
    )  # In WAV files, first 44 bytes are reserved for the header
    print(f"The header is {header}")

    if header[:4] != b"RIFF" or header[8:12] != b"WAVE" or header[12:16] != b"fmt ":
        raise ValueError("Invalid WAV file")

    # Extract relevant information from the header
    header_chunk_id = struct.unpack("4s", header[0:4])[0]
    header_chunk_size = struct.unpack("<I", header[4:8])[0]
    header_chunk_format = struct.unpack("4s", header[8:12])[0]
    format_chunk_id = struct.unpack("4s", header[12:16])[0]
    format_chunk_size = struct.unpack("<I", header[16:20])[0]
    format_code = struct.unpack("<H", header[20:22])[0]
    channels = struct.unpack("<H", header[22:24])[0]
    sample_rate = struct.unpack("<I", header[24:28])[0]
    byte_rate = struct.unpack("<I", header[28:32])[0]
    block_align = struct.unpack("<H", header[32:34])[0]
    sample_width = struct.unpack("<H", header[34:36])[0]
    data_chunk_id = struct.unpack("4s", header[36:40])[0]
    data_chunk_size = struct.unpack("<I", header[40:44])[0]

    return_dict = {
        "header_chunk_id": header_chunk_id,
        "header_chunk_size": header_chunk_size,
        "header_chunk_format": header_chunk_format,
        "format_chunk_id": format_chunk_id,
        "format_chunk_size": format_chunk_size,
        "format_code": format_code,
        "channels": channels,
        "sample_width": sample_width,
        "sample_rate": sample_rate,
        "byte_rate": byte_rate,
        "block_align": block_align,
        "data_chunk_id": data_chunk_id,
        "data_chunk_size": data_chunk_size,
    }

    return return_dict


if __name__ == "__main__":

    # user_auth.make_friends()
    # logger.log(Log(LogType.INFO, "Starting Flask app"))
    # conv_dict = user_auth.create_conversation()
    system("python3 -m flask --app main run --host=0.0.0.0 --port=5000 --debug")
    # test_chatbot(
    #     api_key=getenv("OPENAI_API_KEY"),
    #     conversation_id="6639ea3410a08c3689597981",
    #     db_connector=app_db_connector,
    #     db_name="teachme_main",
    #     logger = logger
    # )
