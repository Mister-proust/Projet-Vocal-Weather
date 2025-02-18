from transformers import AutoTokenizer, AutoModelForTokenClassification

tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")

from transformers import pipeline

ner_pipeline = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

texte = "Quel temps fera-t-il à Paris demain matin ?"

# Extraction des entités nommées
resultats = ner_pipeline(texte)

# Affichage des résultats
for entite in resultats:
    print(f"🔹 {entite['word']} → {entite['entity_group']} (score: {entite['score']:.2f})")
