import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

# Récupère le chemin du répertoire courant du script
current_dir = os.path.dirname(__file__)
audio_file = os.path.join(current_dir, "..", "data", "recording.wav")


def key(env_path) :
    load_dotenv(env_path)
    speech_key = os.getenv("SPEECH_KEY")
    service_region = os.getenv("SPEECH_REGION")
    return speech_key, service_region

async def recognize_speech_from_file(audio_file):
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv("SPEECH_KEY"), region=os.getenv("SPEECH_REGION"))
    speech_config.speech_recognition_language = "fr-FR"
    audio_config = speechsdk.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        return "Aucun texte reconnu."
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        return f"Reconnaissance annulée : {speech_recognition_result.cancellation_details.reason}"


def main() :
    key()
    recognize_speech_from_file()


if __name__ == "__main__" : main()