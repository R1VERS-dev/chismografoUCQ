from pydantic import BaseModel

# Para crear un lugar (entrada del cliente)
class LugarCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    ubicacion: str | None = None
    categoria: str | None = None
    imagen_url: str | None = None

# Para leer un lugar (respuesta del servidor)
class Lugar(LugarCreate):
    id: int

    class Config:
        orm_mode = True
