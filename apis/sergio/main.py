# main.py
import os
import requests
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import crud, models, schemas
from database import SessionLocal, engine, Base

# Carga variables de entorno
load_dotenv()
USER_AGENT = os.getenv("NOMINATIM_USER_AGENT", "mi_app_gallos_queretaro")

# Crear tablas en la BD (solo la primera vez o al cambiar modelos)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Partidos Gallos Querétaro")

# Configurar CORS para permitir comunicación con el panel central
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static & templates setup (frontend minimalista)
BASE_DIR = os.path.dirname(__file__)
static_path = os.path.join(BASE_DIR, "static")
templates_path = os.path.join(BASE_DIR, "templates")
if os.path.isdir(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

# Dependency para obtener sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def ui_root(request: Request):
    """Frontend HTML minimalista (blanco y negro)"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/web", response_class=HTMLResponse)
def ui_web(request: Request):
    """Frontend HTML minimalista (blanco y negro) - endpoint alternativo"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/partidos/", response_model=schemas.Partido)
def crear_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    return crud.create_partido(db=db, partido=partido)

@app.get("/partidos/", response_model=list[schemas.Partido])
def leer_partidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_partidos(db, skip=skip, limit=limit)

@app.get("/partidos/{partido_id}", response_model=schemas.Partido)
def leer_partido(partido_id: int, db: Session = Depends(get_db)):
    db_partido = crud.get_partido(db, partido_id=partido_id)
    if not db_partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return db_partido

@app.get("/partidos/{partido_id}/estadio")
def obtener_coordenadas_estadio(partido_id: int, db: Session = Depends(get_db)):
    """
    Devuelve las coordenadas (lat, lon) y nombre completo del estadio
    correspondiente al partido con ID dado.
    """
    # Obtener partido de la BD
    db_partido = crud.get_partido(db, partido_id=partido_id)
    if not db_partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    # Llamada a Nominatim para geocoding
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": db_partido.estadio,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, params=params, headers=headers, timeout=5)
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Error al contactar servicio de geocoding")

    data = resp.json()
    if not data:
        raise HTTPException(status_code=404, detail="Estadio no encontrado")

    lugar = data[0]
    return {
        "partido_id": partido_id,
        "estadio": db_partido.estadio,
        "latitud": lugar["lat"],
        "longitud": lugar["lon"],
        "display_name": lugar["display_name"]
    }

@app.delete("/partidos/{partido_id}", status_code=204)
def eliminar_partido(partido_id: int, db: Session = Depends(get_db)):
    """
    Elimina un partido de la base de datos.
    Devuelve 204 No Content si se borró, o 404 si no existe.
    """
    partido = crud.delete_partido(db, partido_id=partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return
