# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, Base


# Crear las tablas en la BD (solo la primera vez, o si cambias modelos)
Base.metadata.create_all(bind=engine)

# DEFINICIÓN GLOBAL
app = FastAPI()

# Dependencia para obtener sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"mensaje": "API de partidos Gallos de Querétaro"}

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
