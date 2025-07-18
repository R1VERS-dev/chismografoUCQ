# main.py
import os
from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from dotenv import load_dotenv      # para leer .env
import httpx                       # cliente HTTP asíncrono

import models, schemas, crud
from database import SessionLocal, engine

# 1) Crea las tablas si no existen
models.Base.metadata.create_all(bind=engine)

# 2) Carga las variables de entorno de .env
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise RuntimeError("❌ Debes definir WEATHER_API_KEY en tu .env")

app = FastAPI(title="API Lugares Querétaro")

# 3) Dependencia para obtener sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ————— RUTAS EXISTENTES —————

@app.get("/", tags=["Root"])
def read_root():
    return {"mensaje": "¡API de Lugares Turísticos en Querétaro está en marcha!"}

@app.get("/lugares", response_model=list[schemas.Lugar], tags=["Lugares"])
def listar_lugares(db: Session = Depends(get_db)):
    return crud.get_lugares(db)

@app.post("/lugares", response_model=schemas.Lugar, tags=["Lugares"])
def crear_lugar(lugar: schemas.LugarCreate, db: Session = Depends(get_db)):
    return crud.create_lugar(db, lugar)

@app.get("/lugares/{lugar_id}", response_model=schemas.Lugar, tags=["Lugares"])
def obtener_lugar(lugar_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    lugar = crud.get_lugar(db, lugar_id)
    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return lugar

@app.put("/lugares/{lugar_id}", response_model=schemas.Lugar, tags=["Lugares"])
def actualizar_lugar(lugar_id: int, lugar_data: schemas.LugarCreate, db: Session = Depends(get_db)):
    lugar = crud.update_lugar(db, lugar_id, lugar_data)
    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return lugar

@app.delete("/lugares/{lugar_id}", tags=["Lugares"])
def eliminar_lugar(lugar_id: int, db: Session = Depends(get_db)):
    success = crud.delete_lugar(db, lugar_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return {"mensaje": f"Lugar con ID {lugar_id} eliminado correctamente"}

# ————— NUEVO ENDPOINT: CLIMA —————

@app.get("/lugares/{lugar_id}/clima", tags=["Clima"])
async def obtener_clima(
    lugar_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    # 1) Obtener el registro del lugar
    lugar = crud.get_lugar(db, lugar_id)
    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    # 2) Parsear la ubicación para OWM:
    #    Tomar la parte antes de la coma y añadir el código de país MX
    raw = getattr(lugar, "ubicacion", None) or lugar.nombre
    city_part = raw.split(",")[0].strip()
    ciudad = f"{city_part},MX"

    # 3) Construir la URL de OpenWeatherMap
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={ciudad}&units=metric&appid={WEATHER_API_KEY}"
    )

    # 4) Llamada HTTP asíncrona
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    # 5) Manejo de errores
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Error al consultar clima")

    data = resp.json()

    # 6) Devolver sólo lo necesario
    return {
        "lugar": lugar.nombre,
        "temperatura": data["main"]["temp"],
        "descripcion": data["weather"][0]["description"],
    }
