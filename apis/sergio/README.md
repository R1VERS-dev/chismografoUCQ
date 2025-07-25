# **API de Partidos Gallos de Querétaro**
Una API web construida con FastAPI y Supabase (PostgreSQL) para consultar y administrar partidos inventados de los Gallos Blancos de Querétaro.

🚀 Tecnologías Usadas
---------------------

*   **Python**
    
*   **FastAPI**
    
*   **SQLite**
    
*   **SQLAlchemy**
    
*   **Pydantic**
    
*   **python-dotenv**
    

📂 Estructura del Proyecto
--------------------------

``` 
sergio/
├── .env               # Variables de entorno (cadena de conexión a Supabase)
├── __init__.py        # Marca la carpeta como paquete Python
├── database.py        # Configuración del engine de SQLAlchemy
├── models.py          # Modelos de datos SQLAlchemy (tabla "partidos")
├── schemas.py         # Esquemas Pydantic (validación de datos)
├── crud.py            # Funciones CRUD para la base de datos
├── main.py            # App de FastAPI y definición de endpoints
└── venv/              # Entorno virtual Python

```

⚙️ Instalación y Ejecución
--------------------------
**1. Clonar o acceder al proyecto**
``` 
cd C:\xampp\htdocs\chismografoUCQ\apis\sergio

``` 
**2. Crear y activar entorno virtual**
``` 
python -m venv venv
# Windows (CMD):
venv\Scripts\activate.bat
# PowerShell (tras ajustar política):
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate
``` 
**3. Instalar dependencias**
``` 
pip install fastapi uvicorn sqlalchemy python-dotenv requests
``` 
**4. Configurar variables de entorno**
``` 
DATABASE_URL=sqlite:///./partidos.db
NOMINATIM_USER_AGENT=mi_app_gallos_queretaro
``` 
**5. Levantar el servidor**
``` 
python -m uvicorn main:app --reload
``` 
    

🌐 URLs Importantes
-------------------

*   **Base URL**:http://127.0.0.1:8000
    
*   **Documentación automática (Swagger UI)**:http://127.0.0.1:8000/docs
    

📌 Endpoints
------------
| Método | Ruta               | Descripción                                |
|--------|--------------------|--------------------------------------------|
| GET    | `/`                | Mensaje de bienvenida de la API            |
| POST   | `/partidos/`       | Crear un nuevo partido                     |
| GET    | `/partidos/`       | Obtener lista de todos los partidos        |
| GET    | `/partidos/{id}`   | Obtener datos de un partido por su `id`    |
| GET    | `/partidos/{id}/estadio`   | Obtener coordenadas del estadio (latitud, longitud, nombre)    |
| DELETE    | `/partidos/{id}`   | Eliminar un partido por su `id` (status 204 No Content)    |

**Ejemplo JSON para POST**

```
{
  "equipo_local": "Gallos Blancos",
  "equipo_visitante": "León",
  "fecha": "2025-07-12",
  "hora": "19:00:00",
  "estadio": "La Corregidora, Querétaro",
  "resultado": "2-1"
}
```

🛠️ Descripción de Archivos
---------------------------
| Archivo       | Función                                                                                               |
|---------------|-------------------------------------------------------------------------------------------------------|
| `.env`        | Variables de entorno (ruta a partidos.db, User-Agent para Nominatim)                                                     |
| `database.py` | Inicializa el engine de SQLAlchemy y el `SessionLocal` para las sesiones de base de datos             |
| `models.py`   | Define el modelo `Partido` (SQLAlchemy) con columnas: `id`, `equipo_local`, `equipo_visitante`, `fecha`, `hora`, `estadio`, `resultado` |
| `schemas.py`  | Esquemas Pydantic para validación y serialización: `PartidoBase`, `PartidoCreate`, `Partido`         |
| `crud.py`     | 	Funciones para “Create, Read, Update, Delete” (crear, listar, obtener, eliminar partidos)               |
| `main.py`     | Crea la instancia de FastAPI, registra las rutas/endpoints y arranca la aplicación                    |

🧪 Pruebas
----------

Puedes probar la API con:

*   **Swagger UI**: http://127.0.0.1:8000/docs 

📬 Contacto
-----------

Desarrollado por **Sergio Lara**