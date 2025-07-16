from sqlalchemy import Column, Integer, String, Date, Time, Numeric
from .database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    fecha = Column(Date, index=True)
    hora = Column(Time)
    lugar = Column(String)
    artista_principal = Column(String)
    precio = Column(Numeric(8,2))
    aforo_maximo = Column(Integer)
