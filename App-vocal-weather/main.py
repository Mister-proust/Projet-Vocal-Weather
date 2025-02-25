from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import JSONResponse
import os
import subprocess
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles  # Ajout de cet import
import os
from fastapi.templating import Jinja2Templates
from pydub import AudioSegment
from io import BytesIO

app = FastAPI()

UPLOAD_DIR = 'uploads'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request, "nom_app": "Micro-Météo"})

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Sauvegarde du fichier .webm temporairement
        webm_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(webm_path, "wb") as f:
            f.write(await file.read())

        # Conversion du fichier .webm en .wav avec pydub
        audio = AudioSegment.from_file(webm_path, format="webm")
        wav_path = os.path.join(UPLOAD_DIR, file.filename.replace(".webm", ".wav"))
        audio.export(wav_path, format="wav")

        # Retourne le chemin du fichier converti
        return JSONResponse(content={"message": f"File successfully uploaded and converted to {wav_path}"}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload and convert file: {str(e)}"}, status_code=500)