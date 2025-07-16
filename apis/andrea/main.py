from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Actividades Culturales Querétaro")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"mensaje": "API de actividades culturales en Querétaro"}

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
