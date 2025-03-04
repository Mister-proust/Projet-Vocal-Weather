from __future__ import print_function
import time
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os
import requests
from services.ner_transformers import extract_loc, extract_date, main
import dateparser
import re
from datetime import datetime

load_dotenv()
WEATHER_KEY = os.getenv("YOUR_API_KEY")

# Chargement des variables LOC, DATE et current_date depuis le fichier texte
def load_temp_data():
    UPLOAD_DIR = "./uploads/"
    temp_file_path = os.path.join(UPLOAD_DIR, "temp_data.txt")

    with open(temp_file_path, "r") as temp_file:
        lines = temp_file.readlines()

    LOC = DATE = current_date = None
    for line in lines:
        if line.startswith("LOC="):
            LOC = eval(line.split("=")[1].strip())
        elif line.startswith("DATE="):
            DATE = line.split("=")[1].strip()
        elif line.startswith("current_date="):
            current_date = datetime.strptime(line.split("=")[1].strip(), "%Y-%m-%d").date()

    return LOC, DATE, current_date


# Conversion du format date selon le format souhaité
def format_date(date):
    """Convertit une date en format 'YYYY-MM-DD'."""
    date_match = re.search(r"\d{4}/\d{2}/\d{2}", date)  # YYYY/MM/DD
    
    if not date_match:
        print(f"⚠️ Impossible d'extraire la date dans '{date}'.")
        return None

    parsed_date = dateparser.parse(date_match.group(), settings={"DATE_ORDER": "YMD"})

    if parsed_date:
        return parsed_date.strftime('%Y-%m-%d')
    else:
        print(f"⚠️ Impossible de parser la date dans '{date}'.")
        return None


# Fonction pour récupérer les prévisions météo
async def get_weather_forecast(LOC, DATE):
    LOC, DATE, current_date = load_temp_data()
    
    if isinstance(LOC, list):
        LOC = LOC[0]  
        print(f"Localisation extraite : {LOC}")

    # Formatez la date
    DATE = format_date(DATE)
    print(f"Date formatée : {DATE}")

    # Construction de l'URL API avec la localisation et la clé
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_KEY}&q={LOC}&days=3&aqi=no&alerts=no"
    print(f"URL appelée : {url}")  # Pour vérifier l'URL avant l'appel

    try:
        response = requests.get(url)
        response.raise_for_status()  # Cela lèvera une exception si le status code n'est pas 200

        # Si la réponse est ok, traiter les données météo
        forecast_data = response.json()
        forecast_days = forecast_data.get("forecast", {}).get("forecastday", [])

        if not forecast_days:
            print(f"⚠️ Aucune donnée de prévision reçue pour {LOC}.")
            return {"error": "Aucune donnée météo trouvée pour la localisation"}

        meteo_resultats = []
        for day in forecast_days:
            if day["date"] == DATE:
                meteo_resultats.append({
                    "date": day["date"],
                    "LOC": LOC,
                    "hours": [
                        {
                            "time": hour["time"],
                            "condition": hour["condition"]["icon"],
                            "temp_c": hour["temp_c"],
                            "wind_kph": hour["wind_kph"],
                            "chance_of_rain": hour["chance_of_rain"]
                        }
                        for hour in day["hour"]
                    ]
                })
        if not meteo_resultats:
            print(f"⚠️ Aucune donnée météo disponible pour la date {DATE}.")
            return {"error": f"Aucune donnée météo trouvée pour la date {DATE}"}

        return meteo_resultats
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur dans la requête API : {e}")
        return {"error": "Erreur dans la récupération des données météo"}
