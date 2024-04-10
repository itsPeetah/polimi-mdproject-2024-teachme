from os import system, getenv
from sys import path

path.append("../../")

from dotenv import load_dotenv
from google.cloud import speech
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from elevenlabs.client import ElevenLabs

from LLM import ConversationalChatBot
from database import MongoDBConnector

load_dotenv()

app = Flask(__name__)
CORS(app, origins='*')
speechClient = speech.SpeechClient()
EL_client = ElevenLabs(api_key=getenv("ELEVENLABS_API_KEY"))

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
    
def run_quickstart(audio_stream: bytes) -> speech.RecognizeResponse:
    audio = speech.RecognitionAudio(content=audio_stream)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2,  # 1 channel for raw, 2 channels for wav
        sample_rate_hertz=44100,  # 16000 for raw, 44100 for wav
        language_code="en-US",
    )
    response = speechClient.recognize(config=config, audio=audio)
    
    transcript = response.results[0].alternatives[0].transcript
    
    chatbot = ConversationalChatBot(
        api_key=getenv("OPENAI_API_KEY"),
        conversation_id=1,
        conversation_user_level="intermediate",
        conversation_difficulty="medium",
        conversation_topic="Discussing the weather",
        db_connector=MongoDBConnector(getenv("MONGODB_URI")),
    )

    response = chatbot.send_message(transcript).content
    result = {
          "human" : transcript,
          "chatbot" : response
    }
    print(result)

    return result


if __name__ == "__main__":
    system("python3 -m flask --app main run --host=0.0.0.0 --port=5000")
