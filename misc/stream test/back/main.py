from time import time
from flask import Flask, request, Response
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS

from audio.buffer_handler import BufferHanlder

flask_app = Flask(__name__)
flask_ws = SocketIO(flask_app, cors_allowed_origins="*")
CORS(flask_app)

audio_buffer_handlers = {}

# ROUTES


@flask_app.route("/hello", methods=["GET"])
def route_hello():
    return Response(status=200, response="hello, world".encode("utf-8"))


@flask_app.route("/now", methods=["GET"])
def route_now():
    t_as_int = int(time())
    return str(t_as_int)


@flask_app.route("/flush", methods=["GET"])
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
    is_speaking, was_speaking, max_sample = handler.handle_audio_data(audio_data)
    if not is_speaking and was_speaking:
        print("STOPPED SPEAKING")
        emit(
            "speaking_status",
            f"You stopped speaking (max_sample: {max_sample})",
            to=sid,
        )
    if is_speaking and not was_speaking:
        print("STARTED SPEAKING")
        emit(
            "speaking_status",
            f"You started speaking (max_sample: {max_sample})",
            to=sid,
        )


if __name__ == "__main__":
    flask_ws.run(flask_app, debug=True)
