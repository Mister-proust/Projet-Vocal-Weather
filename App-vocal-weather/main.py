from fastapi import FastAPI, Request, UploadFile, File, Query
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import subprocess
from fastapi.templating import Jinja2Templates
from pydub import AudioSegment
from io import BytesIO
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from time import time
from services.speech_recognition import recognize_speech_from_file, key
from services.conversion import upload_audio
from services.ner_transformers import extract_loc, extract_date, main
from services.Weather_api import get_weather_forecast
from fastapi import FastAPI, Request, UploadFile, File

key(env_path="../.env")

app = FastAPI()

app.mount("/static", StaticFiles(directory="./webapp/static"), name="static")

templates = Jinja2Templates(directory="./webapp/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nom_app": "Micro-Météo"})


@app.post("/upload")
async def convert_text(file: UploadFile = File(...)):
    wav_path = await upload_audio(file)
    recognized_text = await recognize_speech_from_file(wav_path)
    LOC, DATE, current_date = await main(wav_path)
    weather_results = await get_weather_forecast(LOC, DATE)

    # Retourner les résultats sous forme de JSON pour utilisation dans la page
    return JSONResponse(content={"text": recognized_text}, status_code=200)

@app.get("/meteopage", response_class=HTMLResponse)
async def read_meteopage(request: Request, LOC: str = '', DATE: str = ''):
    # Récupérer la météo si les paramètres sont fournis
    weather_results = await get_weather_forecast(LOC, DATE)
    return templates.TemplateResponse("meteopage.html", {"request": request, "weather_results": weather_results, "LOC": LOC, "DATE": DATE })
    

