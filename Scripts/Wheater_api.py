from __future__ import print_function
import time
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os
import requests
from ner_transformers import extract_loc, extract_date, current_date
import dateparser


load_dotenv()
WHEATER_KEY = os.getenv("YOUR_API_KEY")

LOC=extract_loc()
print(LOC)


DATE=str(extract_date())
print(DATE)
DATE_EXACT = dateparser.parse(DATE, settings={"DATE_ORDER": "YMD"})
print(DATE_EXACT)


configuration = weatherapi.Configuration()
configuration.api_key['key'] = WHEATER_KEY


api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
q = 'Tours' # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name. Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to learn more.
dt = '2025-02-18' # date | Date on or after 1st Jan, 2015 in yyyy-MM-dd format


url = f"http://api.weatherapi.com/v1/forecast.json?key={WHEATER_KEY}&q={LOC}&days={current_date}&aqi=no&alerts=no"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Température actuelle :", data["current"]["temp_c"], "°C")
    print("Température ressentie :", data["current"]["feelslike_c"], "°C")
else:
    print("Erreur :", response.status_code)