import time

from os import system, getenv

from lib.llm import ConversationalChatBot
from lib.database import MongoDBConnector
from lib.audio import BufferHanlder

from dotenv import load_dotenv
from google.cloud import speech
from flask import Flask, request, jsonify, Response
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from elevenlabs.client import ElevenLabs

load_dotenv()

app = Flask(__name__)
flask_ws = SocketIO(app, cors_allowed_origins="*")
CORS(app, origins="*")
speechClient = speech.SpeechClient()
EL_client = ElevenLabs(api_key=getenv("ELEVENLABS_API_KEY"))

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


@app.route("/hello", methods=["GET"])
def route_hello():
    return Response(status=200, response="hello, world".encode("utf-8"))


@app.route("/now", methods=["GET"])
def route_now():
    t_as_int = int(time())
    return str(t_as_int)


@app.route("/flush", methods=["GET"])
def flush():
    for k, v in audio_buffer_handlers.items():
        v.save_audio_to_wav()
        v.buffer.clear()
    return "Ok"


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


def get_user_transcript(audio_stream: bytes) -> speech.RecognizeResponse:
    audio = speech.RecognitionAudio(content=audio_stream)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2,  # 1 channel for raw, 2 channels for wav
        sample_rate_hertz=44100,  # 16000 for raw, 44100 for wav
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
        db_connector=MongoDBConnector(getenv("MONGODB_URI")),
    )
    response = chatbot.send_message(prompt).content
    return response


def run_quickstart(audio_stream: bytes) -> speech.RecognizeResponse:
    transcript = get_user_transcript(audio_stream)
    print("User transcript:", transcript)
    emit("transcript", {"user": transcript})
    response = get_chatbot_answer(transcript)
    print("Chatbot answer:", response)
    emit("transcript", {"chatbot": response})


if __name__ == "__main__":
    system("python3 -m flask --app main run --host=0.0.0.0 --port=5000 --debug")