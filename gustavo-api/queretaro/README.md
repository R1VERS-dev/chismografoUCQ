# 🌄 API de Lugares Turísticos de Querétaro

> Una API web construida con **FastAPI**, **Supabase** y **OpenWeatherMap**, que además se expone públicamente vía túnel ngrok.

---

## 🚀 Tecnologías Usadas

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square\&logo=python\&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square\&logo=fastapi\&logoColor=white)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square\&logo=postgresql\&logoColor=white)]()
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square\&logo=supabase\&logoColor=white)]()
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FF0000?style=flat-square\&logo=sqlalchemy\&logoColor=white)]()
[![Pydantic](https://img.shields.io/badge/Pydantic-00BFFF?style=flat-square\&logo=pydantic\&logoColor=white)]()
[![Httpx](https://img.shields.io/badge/HTTPX-000?style=flat-square\&logo=httpx)]()
[![Python-dotenv](https://img.shields.io/badge/python--dotenv-4EA44F?style=flat-square\&logo=python-dotenv)]()
[![Pyngrok](https://img.shields.io/badge/pyngrok-000?style=flat-square\&logo=ngrok)]()

---

## 📂 Estructura del Proyecto

```bash
queretaro/
├── .env               # Variables de entorno (conexión DB, claves externas)
├── database.py        # Configuración del engine de SQLAlchemy
├── models.py          # Modelos de datos SQLAlchemy (tabla `lugares`)
├── schemas.py         # Esquemas Pydantic para validación
├── crud.py            # Funciones CRUD para la base de datos
├── main.py            # App FastAPI: endpoints CRUD + clima
├── tunnel.py          # Script para exponer vía ngrok usando pyngrok
└── venv/              # Entorno virtual
```

---

## ⚙️ Instalación y Ejecución

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu-usuario/queretaro-api.git
   cd queretaro-api
   ```

2. **Crear y activar entorno virtual**

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   ```

3. **Instalar dependencias**

   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv httpx pyngrok
   ```

4. **Configurar variables de entorno**

   * Crear un archivo `.env` en la raíz con:

     ```env
     # Supabase (Session Pooler)
     DATABASE_URL=postgresql://postgres:Diplomado23@aws-0-us-east-2.pooler.supabase.com:5432/postgres

     # Clave gratuita de OpenWeatherMap
     WEATHER_API_KEY=40bc3d00ee3ba35943072e3b0d4bb617

     # Token ngrok (para túnel público)
     NGROK_AUTH_TOKEN=301B2E15ws12vu4CqBzvuUjGgSM_Q53JdehzQQS97KxiLyLW
     ```

5. **Levantar la API local**

   ```bash
   uvicorn main:app --reload
   ```

   * URL base: `http://127.0.0.1:8000`
   * Documentación: `http://127.0.0.1:8000/docs`

6. **Exponer vía ngrok** (en otra terminal)

   ```bash
   python tunnel.py
   ```

   * Obtendrás una URL `https://xxxxx.ngrok-free.app` que redirige a tu `localhost:8000`.

---

## 📌 Endpoints Disponibles

| Método | Ruta                  | Descripción                           |
| ------ | --------------------- | ------------------------------------- |
| GET    | `/`                   | Ruta raíz: mensaje de bienvenida      |
| GET    | `/lugares`            | Listar todos los lugares              |
| POST   | `/lugares`            | Crear un nuevo lugar                  |
| GET    | `/lugares/{id}`       | Obtener un lugar por ID               |
| PUT    | `/lugares/{id}`       | Actualizar un lugar existente         |
| DELETE | `/lugares/{id}`       | Eliminar un lugar por ID              |
| GET    | `/lugares/{id}/clima` | Obtener clima actual (OpenWeatherMap) |

---

## 🔄 Integración con OpenWeatherMap

Al llamar a `/lugares/{id}/clima`, tu API:

1. Lee `ubicacion` desde Supabase (campo String como `"Bernal, Querétaro"`).
2. Extrae la parte antes de la coma y añade `,MX` → `"Bernal,MX"`.
3. Llama a `https://api.openweathermap.org/data/2.5/weather` con:

   * `q=Bernal,MX`
   * `units=metric`
   * `appid=$WEATHER_API_KEY`
4. Devuelve JSON:

   ```json
   {
     "lugar": "Peña de Bernal",
     "temperatura": 23.5,
     "descripcion": "clear sky"
   }
   ```

---

## 🛠️ Descripción de Archivos

| Archivo         | Función                                                     |
| --------------- | ----------------------------------------------------------- |
| **.env**        | Variables sensibles: conexión DB, claves externas, ngrok    |
| **database.py** | Inicializa engine y sesión de SQLAlchemy                    |
| **models.py**   | Define tabla `lugares` con columnas (incluye `ubicacion`)   |
| **schemas.py**  | Modelos Pydantic para validación de peticiones y respuestas |
| **crud.py**     | CRUD básico para `lugares`                                  |
| **main.py**     | FastAPI: CRUD + endpoint `/clima`                           |
| **tunnel.py**   | Script con pyngrok para exponer la API                      |

---

## 🧪 Pruebas y Uso

* **Swagger UI**: `/docs`
* **Postman / HTTP client**:

  ```bash
  curl http://127.0.0.1:8000/lugares/1/clima
  curl https://xxxxx.ngrok-free.app/lugares/1/clima
  ```

---

## 📬 Contacto

Desarrollado por **Gustavo Ríos**
