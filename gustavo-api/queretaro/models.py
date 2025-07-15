from sqlalchemy import Column, Integer, String, Text
from database import Base

class Lugar(Base):
    __tablename__ = "lugares"  # nombre de la tabla en PostgreSQL

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    ubicacion = Column(String)
    categoria = Column(String)
    imagen_url = Column(String)
