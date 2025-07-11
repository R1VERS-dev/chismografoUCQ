from pydantic import BaseModel
from datetime import date, time

class PartidoBase(BaseModel):
    equipo_local: str
    equipo_visitante: str
    fecha: date
    hora: time
    estadio: str
    resultado: str

class PartidoCreate(PartidoBase):
    pass

class Partido(PartidoBase):
    id: int

    class Config:
        orm_mode = True
