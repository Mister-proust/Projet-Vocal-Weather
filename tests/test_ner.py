from Scripts.ner_transformers import truc, extract_entities, extract_loc, extract_date
import datetime
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def test_ner_loc() :
    current_date=datetime.date.today()

    texte = "température 24 février à 12h35 à Tours "

    gemini_key=os.getenv("API_KEY_GEMINI")

    client = genai.Client(api_key=gemini_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f"""Trouve la localisation et transcris en format la ou les dates en sachant qu'on est le : {current_date} 
            le format date doit être YYYY/MM/DD dans le script suivant sans ajouter un seul mot supplémentaire : {texte}
            Si des heures sont retrouvés dans le script, recupère les et mets les en format HH:00 car je ne souhaite pas de minutes"""
    ))

    ner_pipeline = truc() 
    resultats = extract_entities(ner_pipeline, response.text)
    
    LOC = extract_loc(resultats)
    assert LOC == ['Tours']
  

def test_ner_date() :
    current_date=datetime.date.today()

    texte = "température 24 février à Tours "

    gemini_key=os.getenv("API_KEY_GEMINI")

    client = genai.Client(api_key=gemini_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f"""Trouve la localisation et transcris en format la ou les dates en sachant qu'on est le : {current_date} 
            le format date doit être YYYY/MM/DD dans le script suivant sans ajouter un seul mot supplémentaire : {texte}
            Si des heures sont retrouvés dans le script, recupère les et mets les en format HH:00 car je ne souhaite pas de minutes"""
    ))

    ner_pipeline = truc() 
    resultats = extract_entities(ner_pipeline, response.text)
    
    DATE = extract_date(resultats)
    assert DATE == ['2025/02/24']