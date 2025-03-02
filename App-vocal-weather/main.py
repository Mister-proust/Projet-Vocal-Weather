from fastapi import FastAPI, Request, UploadFile, File, Query, Depends
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
from services.speech_recognition import recognize_speech_from_file, key
from services.conversion import upload_audio
from services.ner_transformers import extract_loc, extract_date, main
from services.Weather_api import get_weather_forecast
from fastapi import FastAPI, Request, UploadFile, File
from sqlalchemy.orm import Session, sessionmaker
from Database.db_connection import build_engine
from Database.models.monitoring import Base, schema, Monitoring


engine = build_engine()
Base.metadata.create_all(engine, checkfirst=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Dépendance pour obtenir la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



key(env_path="../.env")

app = FastAPI()

app.mount("/static", StaticFiles(directory="./webapp/static"), name="static")

templates = Jinja2Templates(directory="./webapp/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nom_app": "Micro-Météo"})


@app.post("/upload")
async def convert_text(file: UploadFile = File(...), db: Session = Depends(get_db)):
    wav_path = await upload_audio(file)
    start_time = time()

    recognized_text = await recognize_speech_from_file(wav_path)
    LOC, DATE, current_date, gemini_response = await main(wav_path)

    time_stt = int((time() - start_time) * 1000)

    weather_results = await get_weather_forecast(LOC, DATE)



    # Sauvegarde en base de données
    new_entry = Monitoring(
        texte_origine=recognized_text,
        code_stt="200",
        time_stt=time_stt,
        msg_stt="Transcription réussie",
        loc=LOC,
        date_info=DATE,
        gemini_response=gemini_response
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return JSONResponse(
        content={
            "text": recognized_text,
            "LOC": LOC,
            "DATE": DATE,
            "gemini_response": gemini_response,
            "weather": weather_results
        },
        status_code=200
    )

@app.get("/meteopage", response_class=HTMLResponse)
async def read_meteopage(request: Request, LOC: str = '', DATE: str = ''):
    # Récupérer la météo si les paramètres sont fournis
    weather_results = await get_weather_forecast(LOC, DATE)
    return templates.TemplateResponse("meteopage.html", {"request": request, "weather_results": weather_results, "LOC": LOC, "DATE": DATE })
    

