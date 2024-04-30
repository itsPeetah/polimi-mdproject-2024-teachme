import time
import struct
import io

from os import system, getenv

import numpy as np

from dotenv import load_dotenv
from google.cloud import speech
from flask import (
    Flask,
    request,
    jsonify,
    Response,
    render_template,
    redirect,
    url_for,
    make_response,
)
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from elevenlabs.client import ElevenLabs
from pymongo import MongoClient

from lib.llm import ConversationalChatBot, test_chatbot
from lib.database import MongoDBConnector
from lib.audio import BufferHanlder
from lib.auth import AuthenticationService, UserAuthenticationException
from lib.log import Logger
from lib.log import Log, LogType

load_dotenv()

app = Flask(__name__)
flask_ws = SocketIO(app, cors_allowed_origins="*")
CORS(app, origins="*")
speechClient = speech.SpeechClient()
EL_client = ElevenLabs(api_key=getenv("ELEVENLABS_API_KEY"))
app_db_connector = MongoDBConnector(
    getenv("MONGODB_URI")
)  # TEST if this works otherwise declare global client?
user_auth = AuthenticationService(app_db_connector)
logger = Logger(app_db_connector)

audio_buffer_handlers = {}


# ROUTES


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        # Access uploaded file
        audio_file = request.files["audio_file"]
        # Check if a file was uploaded
        if audio_file:
            # Process the uploaded file
            audio_data = audio_file.stream.read()
            recognized = run_quickstart(audio_data)
            response = jsonify(recognized)
            # response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
            return "No file uploaded!"

    with open("stt_chatbot_tts_integration.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    return html_content


@app.route("/text-to-speech", methods=["GET"])
def text_to_speech():
    text = request.args.get("text")
    audio_tts = EL_client.generate(text=text)
    response = Response(audio_tts, mimetype="audio/wav")
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/logs", methods=["GET"])
def show_all_logs():
    return show_logs(log_type=None)


@app.route("/logs/", methods=["GET"])
def redirect_logs_slash():
    return redirect(url_for("show_all_logs"))


@app.route("/logs/<log_type>", methods=["GET"])
def show_logs(log_type):
    db = app_db_connector.connect("teachme_main")
    logs_collection = db.get_collection("logs")
    if log_type is None:
        logs = logs_collection.retrieve_all()
    else:
        log_type = log_type.upper()
        if log_type == "INFO":
            logs = logs_collection.retrieve_by_log_type(LogType.INFO)
        elif log_type == "ERROR":
            logs = logs_collection.retrieve_by_log_type(LogType.ERROR)
        else:
            return redirect(url_for("show_all_logs"))
    return render_template("logs_template.html", log_type=log_type, logs=logs)


@app.route("/hello", methods=["GET"])
def route_hello():
    return Response(status=200, response="hello, world".encode("utf-8"))


@app.route("/now", methods=["GET"])
def route_now():
    t_as_int = int(time.time())
    return str(t_as_int)


@app.route("/flush", methods=["GET"])
def flush():
    for k, v in audio_buffer_handlers.items():
        v.save_audio_to_wav()
        v.buffer.clear()
    return "Ok"

@app.route("/create-friendship", methods=["POST"])
def create_friendship():
    data = request.get_json()
    teacher_email = data.get("teacher_email")
    student_email = data.get("student_email")
    db = app_db_connector.connect("teachme_main")
    user_data_collection = db.get_collection("user_data")
    user_data_collection.create_friendship_using_email(teacher_email=teacher_email, student_email=student_email) # TODO: add better error management

@app.route("/get-friends", methods=["GET"])
def get_friends():
    data = request.get_json()
    user_email = data.get("user_email")
    db = app_db_connector.connect("teachme_main")
    user_data_collection = db.get_collection("user_data")
    user_friends = user_data_collection.get_user_friends(user_email=user_email)
    return jsonify(user_friends)


# AUTHENTICATION


@app.route("/register", methods=["POST"])
def handle_sign_up():
    try:
        request_data = user_auth.validate_request_data(request, signup=True)
        user = user_auth.register_user(**request_data)
        response = make_response(redirect("/now", 302))
        response.set_cookie(
            key="uid", value=user._id, max_age=60 * 60 * 24 * 10
        )  # TODO Figure this one out
        return response
    except UserAuthenticationException as ex:
        print(ex)
        return redirect("/", 400)


@app.route("/login", methods=["POST"])
def handle_sign_in():
    try:
        request_data = user_auth.validate_request_data(request, signup=False)
        user = user_auth.get_user_by_email(request_data["email"])
        response = make_response(redirect("/now", 302))
        response.set_cookie(
            key="uid", value=user._id, max_age=60 * 60 * 24 * 10
        )  # TODO Figure this one out
        return response
    except UserAuthenticationException as ex:
        print(ex)
        return redirect("/", 400)


@app.route("/me", methods=["GET"])
def handle_is_logged_in():
    # TODO Add Role differentiation
    try:
        uid = request.cookies["uid"]
        print(uid)
        user = user_auth.get_user_by_id(uid)
        return jsonify({"user_id": user._id, "role": user.role})
    except:
        return make_response("KO", 401)


# WEBSOCKET


@flask_ws.on("connect")
def on_connected():
    sid = request.sid
    print("ws user connected", f"sid: {sid}")
    audio_buffer_handlers[sid] = BufferHanlder(sid, 500)


@flask_ws.on("disconnected connect")
def on_connected():
    sid = request.sid
    print("ws user disconnected", f"sid: {sid}")


@flask_ws.on("message")
def on_message(message):
    print("Received message:", message)


@flask_ws.on("foo")
def on_foo_event(data):
    print("FOO", data)


@flask_ws.on("audio_data")
def on_audio_data(data: bytes):
    sid = request.sid
    handler: BufferHanlder = audio_buffer_handlers[sid]
    audio_data = data["data"]
    is_speaking, was_speaking, max_sample, audio_bytes = handler.handle_audio_data(
        audio_data
    )
    if not is_speaking and was_speaking:
        print("STOPPED SPEAKING")
        emit(
            "speaking_status",
            f"You stopped speaking (max_sample: {max_sample})",
            to=sid,
        )
        response = run_quickstart(audio_bytes)
    if is_speaking and not was_speaking:
        print("STARTED SPEAKING")
        emit(
            "speaking_status",
            f"You started speaking (max_sample: {max_sample})",
            to=sid,
        )


@flask_ws.on("transcript_data")
def on_transcript_data(data: str):
    print("\n\n\n\n\n\n", data, end="\n\n\n\n\n\n")
    response = get_chatbot_answer(data)
    print("Chatbot answer:", response)
    emit("chatbot_response", response)


def get_user_transcript(
    audio_stream: bytes,
) -> speech.RecognizeResponse:  # TODO: DEPRECATED TO ADJUST WITH NEW LOGIC
    audio_headers = load_audio(audio_stream)
    print(audio_headers)
    audio = speech.RecognitionAudio(content=audio_stream)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=audio_headers.get(
            "channels"
        ),  # 1 channel for raw, 2 channels for wav
        sample_rate_hertz=audio_headers.get(
            "sample_rate"
        ),  # 16000 for raw, 44100 for wav
        language_code="en-US",
    )
    response = speechClient.recognize(config=config, audio=audio)
    if len(response.results) >= 1:
        transcript: str = response.results[0].alternatives[0].transcript
        return transcript
    else:
        return "Audio transcription failed"


def get_chatbot_answer(prompt: str) -> str:
    chatbot = ConversationalChatBot(
        api_key=getenv("OPENAI_API_KEY"),
        conversation_id=1,
        conversation_user_level="intermediate",
        conversation_difficulty="medium",
        conversation_topic="Discussing the weather",
        db_connector=app_db_connector,
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


def run_quickstart(audio_stream: bytes) -> speech.RecognizeResponse:
    transcript = get_user_transcript(audio_stream)
    print("User transcript:", transcript)
    emit("transcript", {"user": transcript})
    response = get_chatbot_answer(transcript)
    print("Chatbot answer:", response)
    emit("transcript", {"chatbot": response})


if __name__ == "__main__":
    # user_auth.make_friends()
    #logger.log(Log(LogType.INFO, "Starting Flask app"))
    system("python3 -m flask --app main run --host=0.0.0.0 --port=5000 --debug")
    # test_chatbot(
    #     api_key=getenv("OPENAI_API_KEY"),
    #     conversation_id=2123,
    #     conversation_user_level="intermediate",
    #     conversation_difficulty="medium",
    #     conversation_topic="The conversation topic is left free.",
    #     db_connector=app_db_connector,
    #     db_name="teachme_main",
    # )
