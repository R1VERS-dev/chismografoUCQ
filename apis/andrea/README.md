# API de Actividades Culturales en Querétaro
Una API web construida con FastAPI y Supabase (PostgreSQL) para registrar y consultar eventos culturales realizados en Querétaro.

🚀 Tecnologías Usadas
---------------------

* Python
* FastAPI
* PostgreSQL (via Supabase)
* SQLAlchemy
* Pydantic
* python-dotenv

📂 Estructura del Proyecto
--------------------------

andrea/
├── .env               # Variables de entorno (cadena de conexión a Supabase)
├── database.py        # Configuración del engine de SQLAlchemy
├── models.py          # Modelos de datos SQLAlchemy (tabla "eventos")
├── schemas.py         # Esquemas Pydantic (validación de datos)
├── crud.py            # Funciones CRUD para la base de datos
├── main.py            # App de FastAPI y definición de endpoints
├── __init__.py        # Marca la carpeta como paquete Python (opcional)
└── venv/              # Entorno virtual Python

 Instalación y Ejecución
--------------------------

1. Acceder a la carpeta del proyecto:

cd apis/andrea

2. Crear y activar entorno virtual:

python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

3. Instalar dependencias:

pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv

4. Crear archivo .env con:

DATABASE_URL=postgresql://postgres:WhyMe?05@db.mrokqsrimzikilafaptx.supabase.co:5432/postgres

5. Ejecutar servidor:

uvicorn main:app --reload

🌐 URLs Importantes
-------------------

* Base URL: http://127.0.0.1:8000
* Documentación Swagger UI: http://127.0.0.1:8000/docs

📌 Endpoints
------------

| Método | Ruta            | Descripción                                |
|--------|------------------|--------------------------------------------|
| GET    | /                | Mensaje de bienvenida de la API            |
| POST   | /eventos/        | Crear un nuevo evento cultural             |
| GET    | /eventos/        | Obtener lista de todos los eventos         |
| GET    | /eventos/{id}    | Obtener información de un evento por ID    |

🛠 Descripción de Archivos
---------------------------

| Archivo       | Función                                                                                                 |
|---------------|---------------------------------------------------------------------------------------------------------|
| .env          | Variables de entorno con la URL de conexión a la base de datos                                          |
| database.py   | Inicializa el engine de SQLAlchemy y SessionLocal                                                      |
| models.py     | Define el modelo Evento (SQLAlchemy) con columnas: id, nombre, descripción, fecha, hora, lugar, etc.   |
| schemas.py    | Esquemas Pydantic para validación y serialización: EventoBase, EventoCreate, Evento                   |
| crud.py       | Funciones para "Create" y "Read" (crear evento, listar eventos, obtener evento por ID)                |
| main.py       | Crea la instancia de FastAPI, registra rutas y lanza la aplicación                                     |

🧪 Pruebas
----------

Puedes probar la API directamente desde Swagger UI:  
http://127.0.0.1:8000/docs

📩 Contacto
-----------

Desarrollado por Andrea Venegas Chaparro
