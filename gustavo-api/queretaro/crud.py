from sqlalchemy.orm import Session
import models, schemas

# Obtener todos los lugares
def get_lugares(db: Session):
    return db.query(models.Lugar).all()

# Crear un nuevo lugar
def create_lugar(db: Session, lugar: schemas.LugarCreate):
    db_lugar = models.Lugar(
        nombre=lugar.nombre,
        descripcion=lugar.descripcion,
        ubicacion=lugar.ubicacion,
        categoria=lugar.categoria,
        imagen_url=lugar.imagen_url
    )
    db.add(db_lugar)
    db.commit()
    db.refresh(db_lugar)
    return db_lugar

# Obtener lugar por ID
def get_lugar(db: Session, lugar_id: int):
    return db.query(models.Lugar).filter(models.Lugar.id == lugar_id).first()

# Actualizar un lugar
def update_lugar(db: Session, lugar_id: int, lugar_data: schemas.LugarCreate):
    lugar = db.query(models.Lugar).filter(models.Lugar.id == lugar_id).first()
    if lugar:
        lugar.nombre = lugar_data.nombre
        lugar.descripcion = lugar_data.descripcion
        lugar.ubicacion = lugar_data.ubicacion
        lugar.categoria = lugar_data.categoria
        lugar.imagen_url = lugar_data.imagen_url
        db.commit()
        db.refresh(lugar)
    return lugar

# Eliminar un lugar
def delete_lugar(db: Session, lugar_id: int):
    lugar = db.query(models.Lugar).filter(models.Lugar.id == lugar_id).first()
    if lugar:
        db.delete(lugar)
        db.commit()
    return lugar
