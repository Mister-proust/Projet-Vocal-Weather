from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import subprocess
from fastapi.templating import Jinja2Templates
from pydub import AudioSegment
from io import BytesIO
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from time import time
app = FastAPI()


UPLOAD_DIR = './uploads/'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/static", StaticFiles(directory="./webapp/static"), name="static")

templates = Jinja2Templates(directory="./webapp/templates")


# 🔑 Chargement des variables d'environnement
load_dotenv()
SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nom_app": "Micro-Météo"})


@app.post("/upload")
async def upload_audio(file: UploadFile = File()):
    try:
        # Lire le fichier en mémoire
        file_content = await file.read()
        # Vérifier si le fichier est bien reçu
        if not file_content:
            return JSONResponse(content={"message": "Fichier vide reçu"}, status_code=400)

        print(f"Nom du fichier reçu : {file.filename}")  # Debug

        # Tentative de conversion avec pydub
        try:
            audio = AudioSegment.from_file(BytesIO(file_content), format="webm")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {str(e)}")
            return JSONResponse(content={"message": f"Erreur lecture WebM : {str(e)}"}, status_code=500)
        
        # Exportation en WAV
        with BytesIO() as wav_buffer:
            try:
                audio.export(wav_buffer, format="wav")
            except Exception as e:
                print(f"Erreur lors de la conversion en WAV : {str(e)}")
                return JSONResponse(content={"message": f"Erreur conversion WAV : {str(e)}"}, status_code=500)
            wav_path = UPLOAD_DIR + file.filename
            # Sauvegarde du fichier
            wav_buffer.seek(0)
            with open(wav_path, "wb") as wav_file:
                wav_file.write(wav_buffer.read())
            wav_buffer.close()
        recognized_text = recognize_speech_from_file(wav_path)
        print(recognized_text)
        
        return JSONResponse(content={"message": "File converted and processed", "text": recognized_text}, status_code=200)

    except Exception as e:
        print(f"Erreur générale : {str(e)}")  # Ajout du log
        return JSONResponse(content={"message": f"Erreur lors de l'upload : {str(e)}"}, status_code=500)


def recognize_speech_from_file(audio_file):
    """Utilise Azure Speech API pour convertir l'audio en texte."""
    try:
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
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
    except Exception as e:
        return f"Erreur de reconnaissance vocale : {str(e)}"