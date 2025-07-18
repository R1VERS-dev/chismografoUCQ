from sqlalchemy.orm import Session
import models, schemas

def get_eventos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Evento).offset(skip).limit(limit).all()

def get_evento(db: Session, evento_id: int):
    return db.query(models.Evento).filter(models.Evento.id == evento_id).first()

def create_evento(db: Session, evento: schemas.EventoCreate):
    db_evento = models.Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento
