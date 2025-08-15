from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, Base
import os, requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
USER_AGENT = os.getenv("NOMINATIM_USER_AGENT")

# Crear tablas
Base.metadata.create_all(bind=engine)

# App FastAPI
app = FastAPI(title="API Actividades Culturales Querétaro")

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar CORS para permitir comunicación con el panel central
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"mensaje": "API de actividades culturales en Querétaro"}

@app.get("/web", response_class=HTMLResponse)
def web():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.post("/eventos/", response_model=schemas.Evento)
def crear_evento(evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    return crud.create_evento(db=db, evento=evento)

@app.get("/eventos/", response_model=list[schemas.Evento])
def leer_eventos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_eventos(db, skip=skip, limit=limit)

@app.get("/eventos/{evento_id}", response_model=schemas.Evento)
def leer_evento(evento_id: int, db: Session = Depends(get_db)):
    db_evento = crud.get_evento(db, evento_id=evento_id)
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return db_evento

@app.get("/eventos/{evento_id}/coordenadas")
def obtener_coordenadas_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = crud.get_evento(db, evento_id=evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": evento.lugar,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": USER_AGENT
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if not data:
        return {"mensaje": "Coordenadas no encontradas"}

    return {
        "lugar": evento.lugar,
        "lat": data[0]["lat"],
        "lon": data[0]["lon"]
    }

@app.delete("/eventos/{evento_id}")
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = crud.delete_evento(db, evento_id=evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return {"mensaje": "Evento eliminado correctamente"}
