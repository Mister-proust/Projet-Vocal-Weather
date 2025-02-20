# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
  villes = ["Paris", "Tours", "Bordeaux"] # on crée une liste villes
  météo = ["Aujourd'hui", "Demain", "Semaine"]
  return render_template("index.html", nom_app="Vocal Weather", villes=villes, météo=météo) # on passe la liste villes au template via render_template

if __name__ == "__main__":
  app.run(debug=True)