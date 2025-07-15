from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Obtener la conexión a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta raíz
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido mi API de lugares turísticos en Querétaro"}

# Obtener todos los lugares
@app.get("/lugares", response_model=list[schemas.Lugar])
def listar_lugares(db: Session = Depends(get_db)):
    return crud.get_lugares(db)

# Crear un nuevo lugar
@app.post("/lugares", response_model=schemas.Lugar)
def crear_lugar(lugar: schemas.LugarCreate, db: Session = Depends(get_db)):
    return crud.create_lugar(db, lugar)

# Obtener un lugar por ID
@app.get("/lugares/{lugar_id}", response_model=schemas.Lugar)
def obtener_lugar(lugar_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    lugar = crud.get_lugar(db, lugar_id)
    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return lugar

# Actualizar un lugar
@app.put("/lugares/{lugar_id}", response_model=schemas.Lugar)
def actualizar_lugar(lugar_id: int, lugar_data: schemas.LugarCreate, db: Session = Depends(get_db)):
    lugar = crud.update_lugar(db, lugar_id, lugar_data)
    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return lugar

# Eliminar un lugar
@app.delete("/lugares/{lugar_id}")
def eliminar_lugar(lugar_id: int, db: Session = Depends(get_db)):
    lugar = crud.delete_lugar(db, lugar_id)
    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return {"mensaje": f"Lugar con ID {lugar_id} eliminado correctamente"}
