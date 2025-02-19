from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")

ner_pipeline = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")


texte = "température demain à Paris "

resultats = ner_pipeline(texte)

def extract_loc():
    resultats 
    LOC = {entite['word'] for entite in resultats if entite['entity_group'] == 'LOC'}
    return LOC

def extract_date():
    resultats
    DATE = {entite['word'] for entite in resultats if entite['entity_group'] == 'DATE'}
    return DATE

