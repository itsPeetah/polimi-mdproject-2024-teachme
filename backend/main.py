import time
import struct
import io

from os import system, getenv

import numpy as np

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


@flask_ws.on("transcript_data")
def on_transcript_data(data: str):
    print("\n\n\n\n\n\n", data, end="\n\n\n\n\n\n")
    response = get_chatbot_answer(data)
    print("Chatbot answer:", response)
    emit("chatbot_response", response)


def get_user_transcript(audio_stream: bytes) -> speech.RecognizeResponse:
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
        db_connector=MongoDBConnector(getenv("MONGODB_URI")),
    )
    response = chatbot.send_message(prompt).content
    return response


def load_audio(audio_file):
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
    system("python3 -m flask --app main run --host=0.0.0.0 --port=5000 --debug")