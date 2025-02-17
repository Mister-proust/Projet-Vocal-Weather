from __future__ import print_function
import time
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os
import requests

load_dotenv()
WHEATER_KEY = os.getenv("YOUR_API_KEY")
city="Tours"
date="2025-02-18"
pluie = "rain"
soleil = "sun"
vent = "wind"
lever = "sunrise"
coucher = "sunset"
heure = "hour"
par_heure = "hourly"
prochain_jour = "tomorrow"

# Configure API key authorization: ApiKeyAuth
configuration = weatherapi.Configuration()
configuration.api_key['key'] = WHEATER_KEY
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'

# create an instance of the API class
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
q = 'Tours' # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name. Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to learn more.
dt = '2025-02-18' # date | Date on or after 1st Jan, 2015 in yyyy-MM-dd format


url = f"http://api.weatherapi.com/v1/forecast.json?key={WHEATER_KEY}&q={city}&days=3&aqi=no&alerts=no"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Température actuelle :", data["current"]["temp_c"], "°C")
    print("Température ressentie :", data["current"]["feelslike_c"], "°C")
else:
    print("Erreur :", response.status_code)