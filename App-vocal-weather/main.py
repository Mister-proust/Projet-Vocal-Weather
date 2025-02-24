from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request, "nom_app": "Micro-Météo"})


@app.post("/meteo")
async def process_form(request: Request, ville: str = Form(...), horizon: str = Form(...)):
    # Récupérer les données du formulaire
    form_data = await request.form()
    ville = form_data.get("ville")
    horizon = form_data.get("horizon")

    # Ici, on traite les données (par exemple, appeler une API météo)
    # Pour cet exemple, on va simplement renvoyer les données du formulaire
    return {"ville": ville, "horizon": horizon}

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Créer un dossier pour enregistrer les fichiers si ce n'est pas déjà fait
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)

        # Créer un chemin pour le fichier à sauvegarder
        file_location = os.path.join(upload_folder, file.filename)

        # Sauvegarder le fichier
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        return {"message": f"Fichier {file.filename} reçu et sauvegardé avec succès.", "file_location": file_location}
    except Exception as e:
        return {"error": f"Erreur lors du téléchargement du fichier : {str(e)}"}