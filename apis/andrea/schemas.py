from pydantic import BaseModel
from datetime import date, time
from decimal import Decimal

class EventoBase(BaseModel):
    nombre: str
    descripcion: str
    fecha: date
    hora: time
    lugar: str
    artista_principal: str
    precio: Decimal
    aforo_maximo: int

class EventoCreate(EventoBase):
    pass

class Evento(EventoBase):
    id: int

    class Config:
        orm_mode = True
