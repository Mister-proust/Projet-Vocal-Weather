from __future__ import print_function
import time
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os
import requests
from ner_transformers import extract_loc, extract_date, main
import dateparser
import re

LOC, DATE, current_date = main()

load_dotenv()
WHEATER_KEY = os.getenv("YOUR_API_KEY")

DATE_PARTS =  [f"[{val.strip()}]" for val in DATE.split(",")]

def parse_datetime(date_str):

    date_match = re.search(r"\d{4}/\d{2}/\d{2}", date_str)  # YYYY/MM/DD
    
    if not date_match:
        print(f"⚠️ Impossible d'extraire la date dans '{date_str}'.")
        return None

    parsed_date = dateparser.parse(date_match.group(), settings={"DATE_ORDER": "YMD", "TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": False})

    return parsed_date


DATES_EXACTES = [parse_datetime(part.strip()) for part in DATE_PARTS if parse_datetime(part.strip())]

if not DATES_EXACTES:
    print("❌ Aucune date valide trouvée, vérifiez réessayer !")
    exit()

  

configuration = weatherapi.Configuration()
configuration.api_key['key'] = WHEATER_KEY


api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

url = f"http://api.weatherapi.com/v1/forecast.json?key={WHEATER_KEY}&q={LOC}&days=3&aqi=no&alerts=no"
response = requests.get(url)

forecast_data = response.json()

def heure_meteo(day_data, heure=None):
    meteo_resultats = []

    try:
        for hour_data in day_data["hour"]:
            heure = int(hour_data["time"].split()[1].split(":")[0])  # Extraire l'heure
            meteo_resultats.append(
                f"🕘 {heure}h : {hour_data['condition']['icon']}, "
                f" Température :{hour_data['temp_c']}°C, Vitesse du vent : {hour_data['wind_kph']} km/h, "
                f"{hour_data['chance_of_rain']}% de pluie"
            )
    except KeyError as e:
        print(f"⚠️ Problème dans l'audio ! : {e}")
        return "❌ Données météo indisponibles"
    
    return "\n".join(meteo_resultats)

forecast_days = forecast_data["forecast"]["forecastday"]
meteo_resultats = []

for date_exacte in DATES_EXACTES:
    try:
        date_str = date_exacte.strftime("%Y-%m-%d")
        heure_str = date_exacte.hour if date_exacte.hour != 0 else None  # ⚠️ Si 00h, considérer toute la journée

        jour_trouve = next((day for day in forecast_days if day["date"] == date_str), None)

        if not jour_trouve:
            meteo_resultats.append(f"⚠️ Aucune donnée pour {date_str}.")
            continue

        meteo_resultats.append(f"📅 Météo pour {date_str} :\n" + heure_meteo(jour_trouve, heure=heure_str))

    except Exception as e:
        print(f"❌ Erreur lors du traitement de la date {date_str} : {e}")



print("\n\n".join(meteo_resultats))