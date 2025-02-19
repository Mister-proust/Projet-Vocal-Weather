from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import os
from dotenv import load_dotenv
from google import genai
import datetime

load_dotenv()


### Model NER ###
def app_model(model_name="Jean-Baptiste/camembert-ner-with-dates"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    return ner_pipeline

# resultats = ner_pipeline(response.text)
def extract_entities(ner_pipeline, response):
    resultats = ner_pipeline(response)
    return resultats


def extract_loc(resultats):
    LOC = [entite['word'] for entite in resultats if entite['entity_group'] == 'LOC']
    return LOC

def extract_date(resultats):
    DATE = [entite['word'] for entite in resultats if entite['entity_group'] == 'DATE']
    return DATE

def main() : 
    ### Date du jour ###
    current_date=datetime.date.today()

### Texte à analyser ###
    texte = "température lundi prochain à 12h35 à Tours "

### Gemini API ###
    gemini_key=os.getenv("API_KEY_GEMINI")

    client = genai.Client(api_key=gemini_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f"""Trouve la localisation et transcris en format la ou les dates en sachant qu'on est le : {current_date} 
            le format date doit être YYYY/MM/DD dans le script suivant sans ajouter un seul mot supplémentaire : {texte}
            Si des heures sont retrouvés dans le script, recupère les et mets les en format HH:00 car je ne souhaite pas de minutes"""
    ))

    print(response.text)

    ner_pipeline = app_model() 
    resultats = extract_entities(ner_pipeline, response.text)
    LOC = extract_loc(resultats)
    print(LOC)
    DATE = extract_date(resultats)
    print(DATE)

if __name__ == "__main__" : main()