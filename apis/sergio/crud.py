from sqlalchemy.orm import Session
import models, schemas

def get_partidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Partido).offset(skip).limit(limit).all()

def get_partido(db: Session, partido_id: int):
    return db.query(models.Partido).filter(models.Partido.id == partido_id).first()

def create_partido(db: Session, partido: schemas.PartidoCreate):
    db_partido = models.Partido(**partido.dict())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido

def delete_partido(db: Session, partido_id: int):
    partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if partido:
        db.delete(partido)
        db.commit()
    return partido
