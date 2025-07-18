# API de Actividades Culturales en Querétaro

Una API web construida con FastAPI y SQLite para registrar, consultar y ubicar geográficamente eventos culturales realizados en Querétaro.

---

🚀 Tecnologías Usadas
---------------------

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- python-dotenv
- Nominatim API (OpenStreetMap)

---

📂 Estructura del Proyecto
--------------------------

andrea/
├── .env               # Variables de entorno (DB y User Agent)
├── database.py        # Configuración del engine de SQLAlchemy
├── models.py          # Modelos SQLAlchemy (tabla "eventos")
├── schemas.py         # Esquemas Pydantic para validación de datos
├── crud.py            # Funciones CRUD de base de datos
├── main.py            # App FastAPI con definición de endpoints
├── __init__.py        # Marca el módulo como paquete Python (opcional)
└── venv/              # Entorno virtual Python

---

⚙️ Instalación y Ejecución
--------------------------

1. Acceder a la carpeta del proyecto:

```bash
cd apis/andrea
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install fastapi uvicorn sqlalchemy python-dotenv requests
```

4. Crear archivo `.env` con:

```env
DATABASE_URL=sqlite:///./actividades.db
NOMINATIM_USER_AGENT=api-actividades-queretaro
```

5. Ejecutar servidor:

```bash
uvicorn main:app --reload
```

---

🌐 URLs Importantes
-------------------

- Base URL: http://127.0.0.1:8000
- Documentación Swagger UI: http://127.0.0.1:8000/docs

---

📌 Endpoints
------------

| Método | Ruta                                 | Descripción                                               |
|--------|--------------------------------------|-----------------------------------------------------------|
| GET    | /                                    | Mensaje de bienvenida                                     |
| POST   | /eventos/                            | Crear un nuevo evento cultural                            |
| GET    | /eventos/                            | Obtener todos los eventos                                 |
| GET    | /eventos/{id}                        | Obtener un evento por ID                                  |
| DELETE | /eventos/{id}                        | Eliminar un evento por ID                                 |
| GET    | /eventos/{id}/coordenadas            | Obtener coordenadas geográficas del lugar del evento      |

🔎 Ejemplo de JSON para crear evento:

```json
{
  "nombre": "Concierto de Jazz",
  "descripcion": "Evento cultural de música en vivo",
  "fecha": "2025-08-15",
  "hora": "20:00:00",
  "lugar": "Teatro de la Ciudad, Querétaro",
  "artista_principal": "Jazz Band QRO",
  "precio": 250.00,
  "aforo_maximo": 500
}
```

---

🛠 Descripción de Archivos
--------------------------

| Archivo       | Función                                                                                                 |
|---------------|---------------------------------------------------------------------------------------------------------|
| .env          | Variables de entorno: URL de SQLite y User Agent para Nominatim                                         |
| database.py   | Inicializa motor SQLite y SessionLocal                                                                  |
| models.py     | Modelo SQLAlchemy `Evento`: id, nombre, descripción, fecha, hora, lugar, artista, precio, aforo         |
| schemas.py    | Esquemas Pydantic: EventoBase, EventoCreate, Evento                                                     |
| crud.py       | Funciones para crear, leer y eliminar eventos                                                           |
| main.py       | App FastAPI con endpoints de CRUD y obtención de coordenadas                                            |

---

🧪 Pruebas
----------

Puedes probar toda la API desde Swagger UI:  
📎 http://127.0.0.1:8000/docs

---

📬 Contacto
----------

Desarrollado por Andrea Venegas Chaparro

