# from google.co import auth
from dotenv import load_dotenv
from google.cloud import speech
from flask import Flask, request

load_dotenv()

app = Flask(__name__)


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
            return str(recognized)
        else:
            return "No file uploaded!"

    return """
            <form method="POST" enctype="multipart/form-data">
                  <input type="file" name="audio_file" accept="audio/*">  <button type="submit">Upload Audio</button>
            </form>
            """


def run_quickstart(audio_stream: bytes) -> speech.RecognizeResponse:

    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    # gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"
    # uri = "/content/drive/MyDrive/TeachMe/audio_samples/harvard.wav"

    # A RecognitionAudio object contains audio data derived from the resource passed as argument
    # audio = speech.RecognitionAudio(uri=gcs_uri)
    audio = speech.RecognitionAudio(content=audio_stream)
    # with open(uri, 'rb') as f:
    #   audio = speech.RecognitionAudio(content=f.read())

    # A RecognitionConfig object is needed to provide information to the recognizer about how to process the request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2,  # 1 channel for raw, 2 channels for wav
        sample_rate_hertz=44100,  # 16000 for raw, 44100 for wav
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response
