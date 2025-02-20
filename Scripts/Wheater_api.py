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

LOC, DATE, current_date = main()

load_dotenv()
WHEATER_KEY = os.getenv("YOUR_API_KEY")

DATE_EXACT = dateparser.parse(DATE, settings={"DATE_ORDER": "YMD"})
print(DATE_EXACT)


configuration = weatherapi.Configuration()
configuration.api_key['key'] = WHEATER_KEY


api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

url = f"http://api.weatherapi.com/v1/forecast.json?key={WHEATER_KEY}&q={LOC}&days={current_date}&aqi=no&alerts=no"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Température actuelle :", data["current"]["temp_c"], "°C")
    print("Température ressentie :", data["current"]["feelslike_c"], "°C")
else:
    print("Erreur :", response.status_code)