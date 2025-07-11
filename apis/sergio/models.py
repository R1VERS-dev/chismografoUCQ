from sqlalchemy import Column, Integer, String, Date, Time
from database import Base

class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    equipo_local = Column(String, index=True)
    equipo_visitante = Column(String, index=True)
    fecha = Column(Date)
    hora = Column(Time)
    estadio = Column(String)
    resultado = Column(String)
