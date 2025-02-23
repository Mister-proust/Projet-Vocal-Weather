from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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