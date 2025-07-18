from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()


# Leer la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear sesiones para comunicarse con la base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir tablas
Base = declarative_base()
